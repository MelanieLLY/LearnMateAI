"""AI agent for generating quizzes from module content using the Claude API.

This module is the single integration point with Anthropic's Claude API for
quiz generation.  All external API calls are isolated here so that tests can
mock at the module boundary without touching the service or router layers.

The agent accepts both instructor-provided course material and the student's
personal notes, then uses a structured multi-shot prompt to produce a single
quiz dict at the requested difficulty level (Easy, Medium, Hard).

Quizzes contain 5–15 questions with at least 60% multiple-choice and at least
one short-answer question.  Very long inputs are truncated before the API call
to stay within a safe token budget.
"""

import json
import logging
import os

import anthropic

from src.agents.prompts.quiz_prompt import (
    DIFFICULTY_LEVELS,
    QUESTION_TYPES,
    SYSTEM_PROMPT,
    build_quiz_user_message,
)

logger = logging.getLogger(__name__)

MAX_INPUT_CHARS: int = 10_000


_MAX_RETRIES: int = 2


def generate_quiz(
    module_content: str,
    student_notes: str,
    difficulty_level: str = "Medium",
    num_questions: int = 5,
) -> dict:
    """Call the Claude API to generate a structured quiz from module content and student notes.

    The function blends both sources in the prompt to ensure questions draw on
    both the instructor's material and the student's own notes.  Very long
    combined inputs are truncated to ``MAX_INPUT_CHARS`` total before the API
    call to avoid excessive token usage.

    Args:
        module_content: Instructor-provided course material or module description.
        student_notes: The student's personal notes for the module.  May be an
            empty string if the student has not yet uploaded notes.
        difficulty_level: Desired difficulty — one of ``DIFFICULTY_LEVELS``
            (``"Easy"``, ``"Medium"``, ``"Hard"``).  Defaults to ``"Medium"``.
        num_questions: Exact number of questions to generate. Defaults to 5.

    Returns:
        A dict containing:
            - ``"title"`` (str): concise quiz title
            - ``"difficulty_level"`` (str): the level used
            - ``"questions"`` (list[dict]): 5–15 question objects, each with
              ``id``, ``text``, ``question_type``, ``options``, ``correct_answer``,
              ``explanation``

    Raises:
        ValueError: If both *module_content* and *student_notes* are empty
            (after stripping), if *difficulty_level* is not in ``DIFFICULTY_LEVELS``,
            if the Claude response cannot be parsed as JSON, or if the returned
            quiz object fails validation.
        anthropic.APIError: If the Claude API call itself fails.
    """
    if not module_content.strip() and not student_notes.strip():
        raise ValueError(
            "At least one of module_content or student_notes must be non-empty."
        )

    if difficulty_level not in DIFFICULTY_LEVELS:
        raise ValueError(
            f"difficulty_level must be one of {sorted(DIFFICULTY_LEVELS)}, "
            f"got: {difficulty_level!r}"
        )

    module_content, student_notes = _maybe_truncate(module_content, student_notes)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=api_key)

    last_error: Exception | None = None
    for attempt in range(1, _MAX_RETRIES + 1):
        logger.info(
            "Requesting quiz generation from Claude API (difficulty=%s, attempt=%d/%d).",
            difficulty_level,
            attempt,
            _MAX_RETRIES,
        )
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": build_quiz_user_message(
                        module_content, student_notes, difficulty_level, num_questions
                    ),
                }
            ],
            tools=[
                {
                    "name": "generate_quiz_output",
                    "description": "Output the generated quiz.",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "difficulty_level": {"type": "string", "enum": ["Easy", "Medium", "Hard"]},
                            "questions": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "integer"},
                                        "text": {"type": "string"},
                                        "question_type": {"type": "string", "enum": ["multiple_choice", "short_answer"]},
                                        "options": {
                                            "type": ["array", "null"],
                                            "items": {"type": "string"}
                                        },
                                        "correct_answer": {"type": "string"},
                                        "explanation": {"type": "string"}
                                    },
                                    "required": ["id", "text", "question_type", "correct_answer", "explanation"]
                                }
                            }
                        },
                        "required": ["title", "difficulty_level", "questions"]
                    }
                }
            ],
            tool_choice={"type": "tool", "name": "generate_quiz_output"}
        )

        tool_use = next((block for block in message.content if block.type == "tool_use"), None)
        if not tool_use:
            last_error = ValueError(
                f"Claude API returned no tool_use block on attempt {attempt}. "
                f"Response: {message.content}"
            )
            logger.warning(str(last_error))
            continue

        quiz: dict = tool_use.input
        try:
            _validate_and_coerce_quiz(quiz, num_questions)
            logger.info(
                "Generated quiz with %d questions (attempt %d).",
                len(quiz.get("questions", [])),
                attempt,
            )
            return quiz
        except ValueError as exc:
            last_error = exc
            logger.warning(
                "Quiz validation failed on attempt %d/%d: %s",
                attempt,
                _MAX_RETRIES,
                exc,
            )

    raise ValueError(
        f"Quiz generation failed after {_MAX_RETRIES} attempts. "
        f"Last error: {last_error}"
    )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _maybe_truncate(module_content: str, student_notes: str) -> tuple[str, str]:
    """Truncate each input to half of MAX_INPUT_CHARS if the combined length exceeds the limit.

    Args:
        module_content: Raw module content string.
        student_notes: Raw student notes string.

    Returns:
        A ``(module_content, student_notes)`` tuple, possibly truncated.
    """
    if len(module_content) + len(student_notes) > MAX_INPUT_CHARS:
        half = MAX_INPUT_CHARS // 2
        logger.warning(
            "Inputs truncated to %d chars each (combined exceeded %d).",
            half,
            MAX_INPUT_CHARS,
        )
        return module_content[:half], student_notes[:half]
    return module_content, student_notes


def _validate_and_coerce_quiz(quiz: dict, expected_count: int) -> None:
    """Validate and coerce the quiz dict returned by Claude.

    Unlike a pure validator, this function also attempts to *fix* minor
    inconsistencies that Claude occasionally introduces (e.g. returning an
    empty list instead of ``None`` for short-answer options, or returning
    a ``questions`` field as a JSON-encoded string instead of a list).

    Args:
        quiz: Raw dict from Claude's tool-use response (mutated in-place).
        expected_count: The number of questions originally requested.

    Raises:
        ValueError: If the response is not a dict, any required top-level
            field is missing, the question count falls outside the tolerated
            range, the MC/SA ratio constraints cannot be satisfied, or any
            individual question is structurally invalid.
    """
    if not isinstance(quiz, dict):
        raise ValueError(
            f"Expected a JSON object from Claude, got: {type(quiz).__name__}"
        )

    for field in ("title", "questions", "difficulty_level"):
        if field not in quiz:
            raise ValueError(
                f"Quiz response missing required field '{field}': {quiz!r}"
            )

    if not isinstance(quiz["title"], str) or not quiz["title"].strip():
        raise ValueError("Quiz 'title' must be a non-empty string")

    if quiz["difficulty_level"] not in DIFFICULTY_LEVELS:
        raise ValueError(
            f"Quiz 'difficulty_level' must be one of {sorted(DIFFICULTY_LEVELS)}, "
            f"got: {quiz['difficulty_level']!r}"
        )

    # --- Coerce questions if Claude returned it as a JSON string ---
    questions = quiz["questions"]
    if isinstance(questions, str):
        import re
        try:
            clean_str = questions.strip()
            clean_str = re.sub(r"^```(?:json)?\s*", "", clean_str)
            clean_str = re.sub(r"\s*```$", "", clean_str)
            from json_repair import repair_json
            parsed = repair_json(clean_str, return_objects=True)
            if isinstance(parsed, list) and parsed:
                logger.warning(
                    "Claude returned 'questions' as a string; repaired successfully."
                )
                quiz["questions"] = parsed
                questions = parsed
            else:
                raise ValueError("repair_json produced an empty or non-list result")
        except Exception as exc:
            logger.error(
                "Failed to repair 'questions' string: %s\nRaw value:\n%s", exc, questions
            )
            raise ValueError(
                f"Quiz 'questions' was returned as a string and could not be repaired: {exc}"
            ) from exc

    if not isinstance(questions, list):
        raise ValueError(
            f"Quiz 'questions' must be a list, got: {type(questions).__name__}"
        )

    # --- Tolerate ±1 question (Claude occasionally returns one extra/fewer) ---
    min_acceptable = max(1, expected_count - 1)
    max_acceptable = expected_count + 1
    if not (min_acceptable <= len(questions) <= max_acceptable):
        raise ValueError(
            f"Quiz must have {expected_count} (±1) questions, got: {len(questions)}"
        )
    if len(questions) != expected_count:
        logger.warning(
            "Claude returned %d questions instead of %d; using as-is.",
            len(questions),
            expected_count,
        )

    for i, q in enumerate(questions):
        _validate_question(i, q)

    mc_count = sum(1 for q in questions if q["question_type"] == "multiple_choice")
    sa_count = sum(1 for q in questions if q["question_type"] == "short_answer")

    if mc_count / len(questions) < 0.6:
        raise ValueError(
            f"At least 60% of questions must be multiple_choice; "
            f"got {mc_count}/{len(questions)} ({mc_count/len(questions):.0%})"
        )
    if sa_count < 1:
        raise ValueError("At least 1 short_answer question is required")


def _validate_question(index: int, q: dict) -> None:
    """Validate a single question dict from the Claude response.

    Args:
        index: Zero-based position of this question in the list (for error messages).
        q: The question dict to validate.

    Raises:
        ValueError: If any required field is missing, has the wrong type, or
            violates type-specific constraints (MC options count, SA null options).
    """
    for field in ("id", "text", "question_type", "correct_answer", "explanation"):
        if field not in q:
            raise ValueError(
                f"Question {index} missing required field '{field}': {q!r}"
            )

    if not isinstance(q["text"], str) or not q["text"].strip():
        raise ValueError(f"Question {index} 'text' must be a non-empty string")
    if not isinstance(q["correct_answer"], str) or not q["correct_answer"].strip():
        raise ValueError(f"Question {index} 'correct_answer' must be a non-empty string")
    if not isinstance(q["explanation"], str) or not q["explanation"].strip():
        raise ValueError(f"Question {index} 'explanation' must be a non-empty string")

    if q["question_type"] not in QUESTION_TYPES:
        raise ValueError(
            f"Question {index} 'question_type' must be one of {sorted(QUESTION_TYPES)}, "
            f"got: {q['question_type']!r}"
        )

    if q["question_type"] == "multiple_choice":
        options = q.get("options")
        if not isinstance(options, list) or len(options) != 4:
            raise ValueError(
                f"MC question {index} must have exactly 4 options, "
                f"got: {options!r}"
            )
        for j, opt in enumerate(options):
            if not isinstance(opt, str) or not opt.strip():
                raise ValueError(
                    f"MC question {index} option {j} must be a non-empty string"
                )
    else:
        # short_answer: options should be None; coerce empty list [] to None
        raw_options = q.get("options")
        if raw_options == [] or raw_options is None:
            q["options"] = None  # normalise in-place
        elif raw_options is not None:
            raise ValueError(
                f"SA question {index} must have options=None, "
                f"got: {raw_options!r}"
            )
