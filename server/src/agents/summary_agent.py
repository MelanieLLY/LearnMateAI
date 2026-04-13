"""AI agent for generating summaries from module content using the Claude API.

This module is the single integration point with Anthropic's Claude API for
summary generation.  All external API calls are isolated here so that tests
can mock at the module boundary without touching the service or router layers.

The agent accepts both instructor-provided course material and the student's
personal notes, then uses a structured prompt to produce a single summary dict
at the requested Bloom's-aligned comprehension level (Brief, Standard, Detailed).
Very long inputs are truncated before the API call to stay within a safe token budget.
"""

import json
import logging
import os

import anthropic

from src.agents.prompts.summary_prompt import (
    SUMMARY_LEVELS,
    SYSTEM_PROMPT,
    build_summary_user_message,
)

logger = logging.getLogger(__name__)

MAX_INPUT_CHARS: int = 10_000


def generate_summary(
    module_content: str,
    student_notes: str,
    summary_level: str = "Standard",
) -> dict:
    """Call the Claude API to generate a structured summary from module content and student notes.

    The function blends both sources in the prompt so the summary synthesises
    content from both the instructor's material and the student's own notes.
    Very long combined inputs are truncated to ``MAX_INPUT_CHARS`` total before
    the API call to avoid excessive token usage.

    Args:
        module_content: Instructor-provided course material or module description.
        student_notes: The student's personal notes for the module.  May be an
            empty string if the student has not yet uploaded notes.
        summary_level: Desired comprehension depth — one of ``SUMMARY_LEVELS``
            (``"Brief"``, ``"Standard"``, ``"Detailed"``).  Defaults to
            ``"Standard"``.

    Returns:
        A dict containing:
            - ``"title"`` (str): concise title for the summary
            - ``"content"`` (str): the summary text
            - ``"word_count"`` (int): number of words in ``content``
            - ``"summary_level"`` (str): the level used (one of ``SUMMARY_LEVELS``)

    Raises:
        ValueError: If both *module_content* and *student_notes* are empty
            (after stripping whitespace), if *summary_level* is not in
            ``SUMMARY_LEVELS``, if the Claude API response cannot be parsed as
            a JSON object, or if the returned object fails field validation.
        anthropic.APIError: If the Claude API call itself fails.
    """
    if not module_content.strip() and not student_notes.strip():
        raise ValueError(
            "At least one of module_content or student_notes must be non-empty."
        )

    if summary_level not in SUMMARY_LEVELS:
        raise ValueError(
            f"summary_level must be one of {sorted(SUMMARY_LEVELS)}, "
            f"got: {summary_level!r}"
        )

    module_content, student_notes = _maybe_truncate(module_content, student_notes)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=api_key)

    logger.info(
        "Requesting summary generation from Claude API (level=%s).", summary_level
    )
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": build_summary_user_message(
                    module_content, student_notes, summary_level
                ),
            }
        ],
    )

    raw = message.content[0].text
    try:
        summary: dict = json.loads(raw)
    except json.JSONDecodeError as exc:
        logger.error("Claude returned non-JSON response: %s", raw)
        raise ValueError(f"Claude API returned invalid JSON: {raw!r}") from exc

    _validate_summary(summary)
    logger.info("Generated summary with %d words.", summary.get("word_count", 0))
    return summary


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


def _validate_summary(summary: dict) -> None:
    """Validate that the summary dict returned by Claude has the required fields.

    Args:
        summary: Raw dict parsed from Claude's JSON response.

    Raises:
        ValueError: If the response is not a dict, any required field is missing,
            or any value has an incorrect type or out-of-range value.
    """
    if not isinstance(summary, dict):
        raise ValueError(
            f"Expected a JSON object from Claude, got: {type(summary).__name__}"
        )

    for field in ("title", "content", "word_count", "summary_level"):
        if field not in summary:
            raise ValueError(
                f"Summary response missing required field '{field}': {summary!r}"
            )

    if not isinstance(summary["title"], str) or not summary["title"].strip():
        raise ValueError("Summary 'title' must be a non-empty string")
    if not isinstance(summary["content"], str) or not summary["content"].strip():
        raise ValueError("Summary 'content' must be a non-empty string")
    if not isinstance(summary["word_count"], int) or summary["word_count"] <= 0:
        raise ValueError(
            f"Summary 'word_count' must be a positive int, got: {summary['word_count']!r}"
        )
    if summary["summary_level"] not in SUMMARY_LEVELS:
        raise ValueError(
            f"Summary 'summary_level' must be one of {sorted(SUMMARY_LEVELS)}, "
            f"got: {summary['summary_level']!r}"
        )
