"""AI agent for generating flashcards from module content using the Claude API.

This module is the single integration point with Anthropic's Claude API for
flashcard generation. All external API calls are isolated here so that tests
can mock at the module boundary without touching the service or router layers.
"""

import json
import logging
import os

import anthropic

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = """You are an expert educator. Given a piece of learning material,
generate concise question-and-answer flashcards that help students study the key concepts.

Return ONLY a valid JSON array with no extra text. Each element must be an object with
exactly two string fields: "question" and "answer".

Example output format:
[
  {"question": "What is X?", "answer": "X is ..."},
  {"question": "How does Y work?", "answer": "Y works by ..."}
]"""


def generate_flashcards_from_content(content: str) -> list[dict[str, str]]:
    """Call the Claude API to generate flashcards from the given text content.

    Args:
        content: The module description or learning material to generate flashcards from.

    Returns:
        A list of dicts, each with ``"question"`` and ``"answer"`` string keys.

    Raises:
        ValueError: If the Claude API response cannot be parsed as a JSON array.
        anthropic.APIError: If the Claude API call fails.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=api_key)

    logger.info("Requesting flashcard generation from Claude API.")
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Generate flashcards for the following content:\n\n{content}",
            }
        ],
    )

    raw = message.content[0].text
    try:
        flashcards: list[dict[str, str]] = json.loads(raw)
    except json.JSONDecodeError as exc:
        logger.error("Claude returned non-JSON response: %s", raw)
        raise ValueError(f"Claude API returned invalid JSON: {raw!r}") from exc

    logger.info("Generated %d flashcards.", len(flashcards))
    return flashcards
