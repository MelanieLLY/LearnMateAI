"""AI agent for generating flashcards from module content using the Claude API.

This module is the single integration point with Anthropic's Claude API for
flashcard generation.  All external API calls are isolated here so that tests
can mock at the module boundary without touching the service or router layers.

The agent accepts both instructor-provided course material and the student's
personal notes, then uses a multi-shot prompt to produce flashcards at multiple
Bloom's taxonomy levels.  Long inputs are truncated before the API call to stay
within a safe token budget.
"""

import json
import logging
import os

import anthropic

from src.agents.prompts.flashcard_prompt import BLOOM_LEVELS, SYSTEM_PROMPT, build_user_message

logger = logging.getLogger(__name__)

MAX_INPUT_CHARS: int = 10_000


def generate_flashcards(
    module_content: str,
    student_notes: str,
) -> list[dict]:
    """Call the Claude API to generate rich flashcards from module content and student notes.

    The function blends both sources in the prompt so that approximately half the
    generated cards draw from each input.  Very long combined inputs are truncated
    to ``MAX_INPUT_CHARS`` total before the API call to avoid excessive token usage.

    Args:
        module_content: Instructor-provided course material or module description.
        student_notes: The student's personal notes for the module.  May be an
            empty string if the student has not yet uploaded notes.

    Returns:
        A list of dicts, each containing:
            - ``"question"`` (str): the flashcard question
            - ``"answer"`` (str): the flashcard answer
            - ``"difficulty"`` (int, 1–5): 1 = easiest, 5 = hardest
            - ``"bloom_level"`` (str): one of the values in ``BLOOM_LEVELS``

    Raises:
        ValueError: If both *module_content* and *student_notes* are empty
            (after stripping whitespace), if the Claude API response cannot be
            parsed as a JSON array, or if any returned card fails field
            validation.
        anthropic.APIError: If the Claude API call itself fails.
    """
    if not module_content.strip() and not student_notes.strip():
        raise ValueError(
            "At least one of module_content or student_notes must be non-empty."
        )

    module_content, student_notes = _maybe_truncate(module_content, student_notes)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=api_key)

    logger.info("Requesting flashcard generation from Claude API.")
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": build_user_message(module_content, student_notes),
            }
        ],
    )

    raw = message.content[0].text
    try:
        flashcards: list[dict] = json.loads(raw)
    except json.JSONDecodeError as exc:
        logger.error("Claude returned non-JSON response: %s", raw)
        raise ValueError(f"Claude API returned invalid JSON: {raw!r}") from exc

    _validate_flashcards(flashcards)
    logger.info("Generated %d flashcards.", len(flashcards))
    return flashcards


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _maybe_truncate(module_content: str, student_notes: str) -> tuple[str, str]:
    """Truncate each input to half of MAX_INPUT_CHARS if the combined length exceeds the limit.

    Args:
        module_content: Raw module content string.
        student_notes: Raw student notes string.

    Returns:
        A (module_content, student_notes) tuple, possibly truncated.
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


def _validate_flashcards(flashcards: list[dict]) -> None:
    """Validate that each flashcard returned by Claude has the required fields.

    Args:
        flashcards: Raw list parsed from Claude's JSON response.

    Raises:
        ValueError: If the response is not a list, or any card is missing a
            required field or contains an out-of-range value.
    """
    if not isinstance(flashcards, list):
        raise ValueError(
            f"Expected a JSON array from Claude, got: {type(flashcards).__name__}"
        )

    for i, card in enumerate(flashcards):
        for field in ("question", "answer", "difficulty", "bloom_level"):
            if field not in card:
                raise ValueError(f"Card {i} missing required field '{field}': {card!r}")

        if not isinstance(card["question"], str) or not card["question"].strip():
            raise ValueError(f"Card {i} has empty or non-string 'question'")
        if not isinstance(card["answer"], str) or not card["answer"].strip():
            raise ValueError(f"Card {i} has empty or non-string 'answer'")
        if not isinstance(card["difficulty"], int) or not (1 <= card["difficulty"] <= 5):
            raise ValueError(
                f"Card {i} 'difficulty' must be an int between 1 and 5, "
                f"got: {card['difficulty']!r}"
            )
        if card["bloom_level"] not in BLOOM_LEVELS:
            raise ValueError(
                f"Card {i} 'bloom_level' must be one of {sorted(BLOOM_LEVELS)}, "
                f"got: {card['bloom_level']!r}"
            )
