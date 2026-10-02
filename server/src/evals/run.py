"""Eval harness for the flashcard, summary and quiz agents.

Usage (from server/):

    python -m src.evals.run            # mock generation + stub judge, no API key (CI)
    python -m src.evals.run --live     # real agents + LLM judge, needs ANTHROPIC_API_KEY
    python -m src.evals.run --generation mock --judge llm   # grade recorded outputs live

Mock generation patches ``anthropic.Anthropic`` inside the agent modules so the
real agent code (prompt building, tool-output parsing, validation) runs against
recorded tool outputs from ``data/mock_outputs.json``. The run writes
``eval-report.md`` and ``eval-report.json`` to ``--report-dir`` and exits 1 if
any deterministic check or judge threshold fails.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest.mock import patch

from src.agents import flashcard_agent, quiz_agent, summary_agent
from src.evals.checks import (
    CheckResult,
    check_flashcards,
    check_grounding,
    check_quiz,
    check_summary,
)
from src.evals.judge import JUDGE_PASS_SCORE, Judge, JudgeError, LLMJudge, StubJudge

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent / "data"
GOLDEN_SET_PATH = DATA_DIR / "golden_set.json"
MOCK_OUTPUTS_PATH = DATA_DIR / "mock_outputs.json"
DEFAULT_REPORT_DIR = Path("eval_reports")
ARTIFACT_TYPES = ("flashcards", "summary", "quiz")


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


class _RecordedClient:
    """Stands in for ``anthropic.Anthropic`` and replays one recorded tool output."""

    def __init__(self, tool_input: dict) -> None:
        block = SimpleNamespace(type="tool_use", input=json.loads(json.dumps(tool_input)))
        self.messages = SimpleNamespace(create=lambda **_: SimpleNamespace(content=[block]))


@contextmanager
def recorded_agent_client(module: Any, tool_input: dict) -> Iterator[None]:
    """Patch the agent module's Anthropic client to return *tool_input*."""
    with patch.object(module.anthropic, "Anthropic", lambda **_: _RecordedClient(tool_input)):
        yield


def generate(case: dict, artifact_type: str, mock_outputs: dict | None) -> tuple[dict, object]:
    """Run one agent for *case*. Returns (request settings, artifact)."""
    content, notes = case["module_content"], case.get("student_notes", "")
    calls: dict[str, tuple[Any, dict, Callable[[], object]]] = {
        "flashcards": (
            flashcard_agent,
            {},
            lambda: flashcard_agent.generate_flashcards(content, notes),
        ),
        "summary": (
            summary_agent,
            dict(case["summary"]),
            lambda: summary_agent.generate_summary(content, notes, **case["summary"]),
        ),
        "quiz": (
            quiz_agent,
            dict(case["quiz"]),
            lambda: quiz_agent.generate_quiz(content, notes, **case["quiz"]),
        ),
    }
    module, request, call = calls[artifact_type]
    if mock_outputs is None:
        return request, call()
    with recorded_agent_client(module, mock_outputs[case["id"]][artifact_type]):
        return request, call()


def run_checks(case: dict, artifact_type: str, artifact: Any) -> list[CheckResult]:
    expected = case.get("expected", {})
    if artifact_type == "flashcards":
        checks = check_flashcards(artifact)
    elif artifact_type == "summary":
        checks = check_summary(artifact, case["summary"]["summary_level"])
    else:
        quiz = case["quiz"]
        checks = check_quiz(artifact, quiz["num_questions"], quiz["difficulty_level"])
    return checks + check_grounding(artifact, expected, artifact_type)


def evaluate_artifact(
    case: dict, artifact_type: str, judge: Judge, mock_outputs: dict | None
) -> dict:
    """Generate, check and judge one artifact. Never raises for model/output errors."""
    entry: dict[str, Any] = {"case": case["id"], "artifact": artifact_type}
    try:
        request, artifact = generate(case, artifact_type, mock_outputs)
    except Exception as exc:  # agent errors are eval results, not crashes
        logger.warning("Generation failed for %s/%s: %s", case["id"], artifact_type, exc)
        entry["checks"] = [CheckResult(f"{artifact_type}.generation", False, str(exc)).__dict__]
        entry["passed"] = False
        return entry
    checks = run_checks(case, artifact_type, artifact)
    entry["checks"] = [c.__dict__ for c in checks]
    try:
        result = judge.grade(case, artifact_type, request, artifact)
        entry["judge"] = {**result.__dict__, "passed": result.passed}
    except JudgeError as exc:
        entry["judge"] = {"judge": judge.name, "error": str(exc), "passed": False}
    entry["passed"] = all(c.passed for c in checks) and entry["judge"]["passed"]
    return entry


def run_eval(cases: list[dict], judge: Judge, mock_outputs: dict | None) -> dict:
    results = [
        evaluate_artifact(case, artifact_type, judge, mock_outputs)
        for case in cases
        for artifact_type in ARTIFACT_TYPES
    ]
    checks = [c for r in results for c in r["checks"]]
    return {
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "generation": "mock" if mock_outputs is not None else "live",
        "judge": judge.name,
        "judge_pass_score": JUDGE_PASS_SCORE,
        "summary": {
            "artifacts": len(results),
            "artifacts_passed": sum(r["passed"] for r in results),
            "checks": len(checks),
            "checks_passed": sum(c["passed"] for c in checks),
        },
        "results": results,
    }


def render_markdown(report: dict) -> str:
    s = report["summary"]
    lines = [
        "# LearnMateAI Agent Eval Report",
        "",
        f"- Generated: {report['generated_at']}",
        f"- Generation: `{report['generation']}` · Judge: `{report['judge']}` "
        f"(pass score {report['judge_pass_score']}/5 on every dimension)",
        f"- Artifacts passed: **{s['artifacts_passed']}/{s['artifacts']}** · "
        f"Deterministic checks passed: **{s['checks_passed']}/{s['checks']}**",
    ]
    if report["judge"] == "stub":
        lines.append("- Judge scores come from the deterministic stub, not from a model.")
    lines += [
        "",
        "| Case | Artifact | Checks | Relevance | Accuracy | Difficulty | Result |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in report["results"]:
        passed = sum(c["passed"] for c in r["checks"])
        scores = r.get("judge", {}).get("scores", {})
        cells = [str(scores.get(d, "–")) for d in ("relevance", "accuracy", "difficulty_match")]
        status = "✅ pass" if r["passed"] else "❌ fail"
        row = [r["case"], r["artifact"], f"{passed}/{len(r['checks'])}", *cells, status]
        lines.append(f"| {' | '.join(row)} |")
    failures = [(r, c) for r in report["results"] for c in r["checks"] if not c["passed"]]
    judge_failures = [r for r in report["results"] if not r.get("judge", {}).get("passed", True)]
    if failures or judge_failures:
        lines += ["", "## Failures", ""]
        lines += [f"- `{r['case']}` {c['name']}: {c['detail']}" for r, c in failures]
        for r in judge_failures:
            j = r["judge"]
            detail = j.get("error") or json.dumps(j.get("scores"))
            lines.append(f"- `{r['case']}` {r['artifact']} judge: {detail}")
    return "\n".join(lines) + "\n"


def write_report(report: dict, report_dir: Path) -> tuple[Path, Path]:
    report_dir.mkdir(parents=True, exist_ok=True)
    json_path, md_path = report_dir / "eval-report.json", report_dir / "eval-report.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    return json_path, md_path


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--live", action="store_true", help="shorthand for --generation live --judge llm"
    )
    parser.add_argument("--generation", choices=["mock", "live"], default="mock")
    parser.add_argument("--judge", choices=["stub", "llm"], default="stub")
    parser.add_argument("--case", action="append", help="only run this case id (repeatable)")
    parser.add_argument("--report-dir", type=Path, default=DEFAULT_REPORT_DIR)
    args = parser.parse_args(argv)
    if args.live:
        args.generation, args.judge = "live", "llm"
    return args


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s")
    args = parse_args(argv)
    if args.generation == "live" or args.judge == "llm":
        from dotenv import load_dotenv

        load_dotenv()
        if not os.environ.get("ANTHROPIC_API_KEY"):
            logger.error("ANTHROPIC_API_KEY is required for --generation live or --judge llm.")
            return 2
    cases = load_json(GOLDEN_SET_PATH)["cases"]
    if args.case:
        cases = [c for c in cases if c["id"] in set(args.case)]
    mock_outputs = load_json(MOCK_OUTPUTS_PATH)["outputs"] if args.generation == "mock" else None
    judge: Judge = LLMJudge() if args.judge == "llm" else StubJudge()
    report = run_eval(cases, judge, mock_outputs)
    json_path, md_path = write_report(report, args.report_dir)
    s = report["summary"]
    sys.stdout.write(
        f"Eval {report['generation']}/{report['judge']}: "
        f"{s['artifacts_passed']}/{s['artifacts']} artifacts, "
        f"{s['checks_passed']}/{s['checks']} checks passed. "
        f"Report: {md_path} ({json_path.name})\n"
    )
    return 0 if s["artifacts_passed"] == s["artifacts"] else 1


if __name__ == "__main__":
    sys.exit(main())
