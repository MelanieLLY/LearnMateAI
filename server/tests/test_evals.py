"""Tests for the agent eval harness (src/evals). No real Claude API calls."""

import copy
import json
from types import SimpleNamespace

import anthropic
import httpx
import pytest

from src.evals import run as eval_run
from src.evals.checks import check_flashcards, check_grounding, check_quiz, check_summary
from src.evals.judge import JUDGE_SCHEMA, JudgeError, LLMJudge, StubJudge, parse_judge_output

GOLDEN = eval_run.load_json(eval_run.GOLDEN_SET_PATH)
MOCKS = eval_run.load_json(eval_run.MOCK_OUTPUTS_PATH)["outputs"]
CASE = GOLDEN["cases"][0]
QUIZ = MOCKS[CASE["id"]]["quiz"]
CARDS = MOCKS[CASE["id"]]["flashcards"]["flashcards"]
SUMMARY = MOCKS[CASE["id"]]["summary"]
GOOD_JUDGE_JSON = json.dumps(
    {
        "relevance": {"score": 5, "rationale": "Covers the module."},
        "accuracy": {"score": 4, "rationale": "Correct."},
        "difficulty_match": {"score": 3, "rationale": "Roughly medium."},
        "unsupported_claims": [],
    }
)


def failed(results):
    return {r.name for r in results if not r.passed}


# ---------------------------------------------------------------------------
# End-to-end mock run
# ---------------------------------------------------------------------------


def test_mock_run_passes_every_golden_artifact():
    report = eval_run.run_eval(GOLDEN["cases"], StubJudge(), MOCKS)

    summary = report["summary"]
    assert summary["artifacts"] == len(GOLDEN["cases"]) * len(eval_run.ARTIFACT_TYPES)
    assert summary["artifacts_passed"] == summary["artifacts"]
    assert summary["checks_passed"] == summary["checks"]


def test_mock_run_goes_through_real_agent_validation():
    broken = copy.deepcopy(MOCKS)
    broken[CASE["id"]]["quiz"]["questions"][0]["options"] = ["only", "three", "options"]

    entry = eval_run.evaluate_artifact(CASE, "quiz", StubJudge(), broken)

    assert entry["passed"] is False
    assert entry["checks"][0]["name"] == "quiz.generation"
    assert "4 options" in entry["checks"][0]["detail"]


def test_main_writes_report_files(tmp_path, capsys):
    exit_code = eval_run.main(["--report-dir", str(tmp_path)])

    assert exit_code == 0
    report = json.loads((tmp_path / "eval-report.json").read_text())
    assert report["generation"] == "mock" and report["judge"] == "stub"
    assert "Agent Eval Report" in (tmp_path / "eval-report.md").read_text()
    assert "9/9 artifacts" in capsys.readouterr().out


def test_main_refuses_live_judge_without_api_key(monkeypatch, tmp_path):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setattr("dotenv.load_dotenv", lambda *a, **k: False)

    assert eval_run.main(["--judge", "llm", "--report-dir", str(tmp_path)]) == 2
    assert not (tmp_path / "eval-report.json").exists()


# ---------------------------------------------------------------------------
# Deterministic checks catch bad outputs
# ---------------------------------------------------------------------------


def test_quiz_checks_pass_on_golden_mock():
    assert failed(check_quiz(QUIZ, 5, "Medium")) == set()


def test_quiz_count_outside_tolerance_fails():
    assert "quiz.count_within_tolerance" in failed(check_quiz(QUIZ, 8, "Medium"))
    assert "quiz.count_within_tolerance" not in failed(check_quiz(QUIZ, 6, "Medium"))


def test_quiz_mc_ratio_and_short_answer_rules():
    all_sa = copy.deepcopy(QUIZ)
    for q in all_sa["questions"][:3]:
        q.update(question_type="short_answer", options=None)
    all_mc = copy.deepcopy(QUIZ)
    all_mc["questions"][-1].update(
        question_type="multiple_choice", options=["a", "b", "c", "d"], correct_answer="a"
    )

    assert "quiz.mc_ratio" in failed(check_quiz(all_sa, 5, "Medium"))
    assert "quiz.min_short_answer" in failed(check_quiz(all_mc, 5, "Medium"))


def test_quiz_answer_must_be_one_of_the_options():
    bad = copy.deepcopy(QUIZ)
    bad["questions"][0]["correct_answer"] = "Something else"
    bad["questions"][1]["options"][1] = bad["questions"][1]["options"][0]

    problems = failed(check_quiz(bad, 5, "Medium"))
    assert {"quiz.mc_answer_in_options", "quiz.mc_options"} <= problems


def test_quiz_difficulty_mismatch_and_schema_errors():
    bad = copy.deepcopy(QUIZ)
    del bad["questions"][0]["explanation"]

    problems = failed(check_quiz(bad, 5, "Hard"))
    assert {"quiz.schema", "quiz.difficulty_matches"} <= problems


def test_flashcard_checks():
    assert failed(check_flashcards(CARDS)) == set()
    same_level = [{**c, "bloom_level": "Remember"} for c in CARDS]
    dupes = CARDS + [CARDS[0]]
    too_few = CARDS[:2]

    assert "flashcards.bloom_spread" in failed(check_flashcards(same_level))
    assert "flashcards.no_duplicates" in failed(check_flashcards(dupes))
    assert "flashcards.count" in failed(check_flashcards(too_few))


def test_summary_checks():
    assert failed(check_summary(SUMMARY, "Standard")) == set()
    wrong_count = {**SUMMARY, "word_count": SUMMARY["word_count"] * 2}

    assert "summary.word_count_accurate" in failed(check_summary(wrong_count, "Standard"))
    assert "summary.length_in_band" in failed(check_summary(SUMMARY, "Brief"))
    assert "summary.level_matches" in failed(check_summary(SUMMARY, "Detailed"))


def test_grounding_flags_forbidden_terms_and_low_coverage():
    expected = {"key_terms": ["photosynthesis", "chlorophyll"], "forbidden_terms": ["relu"]}

    assert failed(check_grounding(QUIZ, expected, "quiz")) == {
        "quiz.key_term_coverage",
        "quiz.no_forbidden_terms",
    }


# ---------------------------------------------------------------------------
# LLM judge (mocked client)
# ---------------------------------------------------------------------------


class FakeClient:
    def __init__(self, text=GOOD_JUDGE_JSON, stop_reason="end_turn"):
        self.calls = []
        block = SimpleNamespace(type="text", text=text)
        response = SimpleNamespace(stop_reason=stop_reason, content=[block])
        self.messages = SimpleNamespace(create=lambda **kw: self.calls.append(kw) or response)


def test_llm_judge_uses_structured_output_and_parses_scores(monkeypatch):
    monkeypatch.delenv("EVAL_JUDGE_MODEL", raising=False)
    client = FakeClient()

    result = LLMJudge(client=client).grade(CASE, "quiz", CASE["quiz"], QUIZ)

    params = client.calls[0]
    assert params["model"] == "claude-opus-5-5"
    assert params["output_config"]["format"] == {"type": "json_schema", "schema": JUDGE_SCHEMA}
    assert "tool_choice" not in params
    assert CASE["module_content"] in params["messages"][0]["content"]
    assert result.scores == {"relevance": 5, "accuracy": 4, "difficulty_match": 3}
    assert result.passed is True


def test_llm_judge_model_can_be_overridden(monkeypatch):
    monkeypatch.setenv("EVAL_JUDGE_MODEL", "claude-sonnet-5-5")
    client = FakeClient()

    LLMJudge(client=client).grade(CASE, "summary", CASE["summary"], SUMMARY)

    assert client.calls[0]["model"] == "claude-sonnet-5-5"


def test_llm_judge_rejects_out_of_range_scores_and_refusals():
    bad = json.loads(GOOD_JUDGE_JSON)
    bad["accuracy"]["score"] = 7

    with pytest.raises(JudgeError, match="accuracy"):
        LLMJudge(client=FakeClient(json.dumps(bad))).grade(CASE, "quiz", {}, QUIZ)
    with pytest.raises(JudgeError, match="refusal"):
        LLMJudge(client=FakeClient(stop_reason="refusal")).grade(CASE, "quiz", {}, QUIZ)


def test_judge_low_score_fails_the_artifact():
    low = json.loads(GOOD_JUDGE_JSON)
    low["relevance"]["score"] = 2

    assert parse_judge_output(json.dumps(low), "llm").passed is False


def test_llm_judge_request_on_the_wire():
    """Send through the real SDK with a mock transport to check headers and body."""
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["headers"] = dict(request.headers)
        captured["body"] = json.loads(request.content)
        message = {
            "id": "msg_test",
            "type": "message",
            "role": "assistant",
            "model": "claude-opus-5-5",
            "stop_reason": "end_turn",
            "content": [{"type": "text", "text": GOOD_JUDGE_JSON}],
            "usage": {"input_tokens": 1, "output_tokens": 1},
        }
        return httpx.Response(200, json=message)

    client = anthropic.Anthropic(
        api_key="test-key", http_client=httpx.Client(transport=httpx.MockTransport(handler))
    )
    result = LLMJudge(client=client, model="claude-opus-5-5").grade(CASE, "quiz", {}, QUIZ)

    assert result.passed is True
    assert captured["headers"]["anthropic-beta"] == "server-side-fallback-2026-07-01"
    assert captured["body"]["fallbacks"] == "default"
    assert captured["body"]["output_config"]["format"]["type"] == "json_schema"
    assert "tool_choice" not in captured["body"]
