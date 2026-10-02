"""Deterministic checks for flashcard, summary and quiz agent outputs.

Each check returns a ``CheckResult``. The quiz thresholds are imported from
``src.agents.quiz_agent`` so the harness and the agent enforce the same rules.
These checks need no model calls and run in CI.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from pydantic import ValidationError

from src.agents.prompts.flashcard_prompt import BLOOM_LEVELS
from src.agents.prompts.summary_prompt import SUMMARY_LEVELS
from src.agents.quiz_agent import (
    MC_OPTION_COUNT,
    MIN_MC_RATIO,
    MIN_SHORT_ANSWER,
    QUESTION_COUNT_TOLERANCE,
)
from src.schemas.quiz import QuizQuestion

# Flashcard rules from flashcard_prompt.SYSTEM_PROMPT ("between 5 and 10").
FLASHCARD_MIN_COUNT = 5
FLASHCARD_MAX_COUNT = 10
FLASHCARD_MIN_BLOOM_LEVELS = 3

# Word targets from summary_prompt.SYSTEM_PROMPT, with slack for model drift.
SUMMARY_WORD_TARGETS: dict[str, tuple[int, int]] = {
    "Brief": (50, 100),
    "Standard": (150, 250),
    "Detailed": (300, 500),
}
SUMMARY_WORD_SLACK = 0.2
SUMMARY_WORD_COUNT_TOLERANCE = 0.15

DEFAULT_MIN_KEY_TERM_COVERAGE = 0.5


@dataclass(frozen=True)
class CheckResult:
    """Outcome of one deterministic check."""

    name: str
    passed: bool
    detail: str


def _result(name: str, passed: bool, detail: str) -> CheckResult:
    return CheckResult(name=name, passed=passed, detail=detail)


def artifact_text(artifact: object) -> str:
    """Flatten an agent output (dict/list/str) into one lowercase string."""
    if isinstance(artifact, str):
        return artifact.lower()
    if isinstance(artifact, dict):
        return " ".join(artifact_text(v) for v in artifact.values())
    if isinstance(artifact, list):
        return " ".join(artifact_text(v) for v in artifact)
    return str(artifact).lower()


def key_term_coverage(text: str, key_terms: list[str]) -> float:
    """Fraction of *key_terms* that appear in *text* (case-insensitive)."""
    if not key_terms:
        return 1.0
    hits = sum(1 for term in key_terms if term.lower() in text)
    return hits / len(key_terms)


def check_grounding(artifact: object, expected: dict, prefix: str) -> list[CheckResult]:
    """Key-term coverage and forbidden-term checks shared by all artifact types."""
    text = artifact_text(artifact)
    key_terms = expected.get("key_terms", [])
    minimum = expected.get("min_key_term_coverage", DEFAULT_MIN_KEY_TERM_COVERAGE)
    coverage = key_term_coverage(text, key_terms)
    found_forbidden = [t for t in expected.get("forbidden_terms", []) if t.lower() in text]
    return [
        _result(
            f"{prefix}.key_term_coverage",
            coverage >= minimum,
            f"{coverage:.0%} of {len(key_terms)} key terms (min {minimum:.0%})",
        ),
        _result(
            f"{prefix}.no_forbidden_terms",
            not found_forbidden,
            f"found {found_forbidden}" if found_forbidden else "none found",
        ),
    ]


def check_quiz(quiz: dict, requested_count: int, requested_difficulty: str) -> list[CheckResult]:
    """Schema, count tolerance, MC ratio and option rules for a quiz dict."""
    questions = quiz.get("questions") if isinstance(quiz, dict) else None
    if not isinstance(questions, list) or not questions:
        return [_result("quiz.schema", False, "quiz has no questions list")]

    schema_errors = []
    for i, q in enumerate(questions):
        try:
            QuizQuestion.model_validate(q)
        except ValidationError as exc:
            schema_errors.append(f"q{i}: {exc.error_count()} error(s)")
    mc = [q for q in questions if q.get("question_type") == "multiple_choice"]
    sa = [q for q in questions if q.get("question_type") == "short_answer"]
    ids = [q.get("id") for q in questions]
    bad_options = [
        q.get("id")
        for q in mc
        if not isinstance(q.get("options"), list)
        or len(q["options"]) != MC_OPTION_COUNT
        or len(set(q["options"])) != MC_OPTION_COUNT
    ]
    answer_missing = [
        q.get("id") for q in mc if q.get("correct_answer") not in (q.get("options") or [])
    ]
    sa_with_options = [q.get("id") for q in sa if q.get("options")]
    count_diff = abs(len(questions) - requested_count)
    ratio = len(mc) / len(questions)

    return [
        _result("quiz.schema", not schema_errors, "; ".join(schema_errors) or "all valid"),
        _result(
            "quiz.count_within_tolerance",
            count_diff <= QUESTION_COUNT_TOLERANCE,
            f"{len(questions)} questions, requested {requested_count} "
            f"(±{QUESTION_COUNT_TOLERANCE})",
        ),
        _result(
            "quiz.mc_ratio",
            ratio >= MIN_MC_RATIO,
            f"{len(mc)}/{len(questions)} multiple choice = {ratio:.0%} (min {MIN_MC_RATIO:.0%})",
        ),
        _result(
            "quiz.min_short_answer",
            len(sa) >= MIN_SHORT_ANSWER,
            f"{len(sa)} short answer (min {MIN_SHORT_ANSWER})",
        ),
        _result(
            "quiz.mc_options",
            not bad_options,
            f"bad option sets in ids {bad_options}"
            if bad_options
            else f"all MC have {MC_OPTION_COUNT} unique options",
        ),
        _result(
            "quiz.mc_answer_in_options",
            not answer_missing,
            f"answer not among options in ids {answer_missing}" if answer_missing else "ok",
        ),
        _result(
            "quiz.sa_options_empty",
            not sa_with_options,
            f"SA with options in ids {sa_with_options}" if sa_with_options else "ok",
        ),
        _result("quiz.unique_ids", len(set(ids)) == len(ids), f"ids {ids}"),
        _result(
            "quiz.difficulty_matches",
            quiz.get("difficulty_level") == requested_difficulty,
            f"got {quiz.get('difficulty_level')!r}, requested {requested_difficulty!r}",
        ),
    ]


def check_flashcards(cards: list[dict]) -> list[CheckResult]:
    """Count, field validity, Bloom spread and duplicate checks for flashcards."""
    if not isinstance(cards, list) or not cards:
        return [_result("flashcards.count", False, "no flashcards")]
    invalid = [
        i
        for i, c in enumerate(cards)
        if not isinstance(c.get("difficulty"), int)
        or not 1 <= c["difficulty"] <= 5
        or c.get("bloom_level") not in BLOOM_LEVELS
        or not str(c.get("question", "")).strip()
        or not str(c.get("answer", "")).strip()
    ]
    levels = {c.get("bloom_level") for c in cards}
    questions = [re.sub(r"\s+", " ", str(c.get("question", "")).strip().lower()) for c in cards]
    return [
        _result(
            "flashcards.count",
            FLASHCARD_MIN_COUNT <= len(cards) <= FLASHCARD_MAX_COUNT,
            f"{len(cards)} cards (expected {FLASHCARD_MIN_COUNT}-{FLASHCARD_MAX_COUNT})",
        ),
        _result("flashcards.fields_valid", not invalid, f"invalid card indexes {invalid}"),
        _result(
            "flashcards.bloom_spread",
            len(levels) >= FLASHCARD_MIN_BLOOM_LEVELS,
            f"{len(levels)} distinct Bloom levels (min {FLASHCARD_MIN_BLOOM_LEVELS})",
        ),
        _result(
            "flashcards.no_duplicates",
            len(set(questions)) == len(questions),
            f"{len(questions) - len(set(questions))} duplicate question(s)",
        ),
    ]


def check_summary(summary: dict, requested_level: str) -> list[CheckResult]:
    """Level, length band and self-reported word count checks for a summary."""
    content = str(summary.get("content", ""))
    actual_words = len(content.split())
    reported = summary.get("word_count")
    level = summary.get("summary_level")
    low, high = SUMMARY_WORD_TARGETS.get(requested_level, (1, 10_000))
    low_ok, high_ok = int(low * (1 - SUMMARY_WORD_SLACK)), int(high * (1 + SUMMARY_WORD_SLACK))
    count_ok = (
        isinstance(reported, int)
        and actual_words > 0
        and abs(reported - actual_words) / actual_words <= SUMMARY_WORD_COUNT_TOLERANCE
    )
    return [
        _result(
            "summary.level_matches",
            level == requested_level and level in SUMMARY_LEVELS,
            f"got {level!r}, requested {requested_level!r}",
        ),
        _result(
            "summary.length_in_band",
            low_ok <= actual_words <= high_ok,
            f"{actual_words} words (target {low}-{high}, accepted {low_ok}-{high_ok})",
        ),
        _result(
            "summary.word_count_accurate",
            count_ok,
            f"reported {reported}, actual {actual_words} "
            f"(tolerance {SUMMARY_WORD_COUNT_TOLERANCE:.0%})",
        ),
    ]
