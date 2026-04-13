"""
RED-phase tests for the FlashcardAgent generate_flashcards function.

Tests are written BEFORE the implementation exists (pure TDD).
Running these against the current codebase must FAIL — that is the expected
RED state.

Covered scenarios
-----------------
1. Happy path       : dual inputs → 5-10 flashcards with question, answer, difficulty, bloom_level
2. Empty input      : both empty strings → raises ValueError before any API call
3. Content integration: user message sent to Claude contains both module_content and student_notes
4. Bloom's variety  : returned flashcards contain ≥3 distinct bloom_level values
5. Long input       : 5000+ char inputs handled gracefully, returns valid list
6. JSON failure     : Claude returns non-JSON → agent raises ValueError
7. Service mapping  : generate_and_store_flashcards maps difficulty & bloom_level into ORM
"""

import json
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.agents.flashcard_agent import generate_flashcards

# ---------------------------------------------------------------------------
# Shared fixtures and helpers
# ---------------------------------------------------------------------------

MODULE_CONTENT = (
    "Machine learning is a subset of artificial intelligence. "
    "Supervised learning uses labelled data. Unsupervised learning finds patterns without labels."
)
STUDENT_NOTES = (
    "Gradient descent minimises the loss function. "
    "Backpropagation computes gradients. Overfitting can be reduced with dropout."
)

RICH_MOCK_FLASHCARDS = [
    {
        "question": "What is supervised learning?",
        "answer": "It uses labelled data to train a model.",
        "difficulty": 1,
        "bloom_level": "Remember",
    },
    {
        "question": "How does gradient descent minimise the loss function?",
        "answer": "It iteratively adjusts weights in the negative gradient direction.",
        "difficulty": 3,
        "bloom_level": "Understand",
    },
    {
        "question": "Apply dropout to reduce overfitting in a neural network.",
        "answer": "Add Dropout layers after dense layers during training.",
        "difficulty": 4,
        "bloom_level": "Apply",
    },
    {
        "question": "What is backpropagation?",
        "answer": "A method to compute gradients through the network via the chain rule.",
        "difficulty": 2,
        "bloom_level": "Remember",
    },
    {
        "question": "When does unsupervised learning apply?",
        "answer": "When you have data without labels and want to find hidden structure.",
        "difficulty": 2,
        "bloom_level": "Understand",
    },
]


def _make_mock_client(flashcards: list[dict]) -> tuple[MagicMock, MagicMock]:
    """Return (mock_anthropic_class, mock_client) pre-wired with a JSON response.

    Args:
        flashcards: List of dicts to serialise as the mocked Claude response.

    Returns:
        A tuple of (mock_anthropic_cls, mock_client) ready for use with patch().
    """
    mock_message = MagicMock()
    mock_message.content = [MagicMock()]
    mock_message.content[0].text = json.dumps(flashcards)

    mock_client = MagicMock()
    mock_client.messages.create.return_value = mock_message

    mock_anthropic_cls = MagicMock(return_value=mock_client)
    return mock_anthropic_cls, mock_client


# ---------------------------------------------------------------------------
# Test 1 — Happy path
# ---------------------------------------------------------------------------


class TestHappyPath:
    """generate_flashcards returns rich flashcards for valid dual input."""

    def test_returns_list_of_dicts(self) -> None:
        """Result is a non-empty list with at most 10 items."""
        mock_cls, _ = _make_mock_client(RICH_MOCK_FLASHCARDS)
        with patch("src.agents.flashcard_agent.anthropic.Anthropic", mock_cls):
            result = generate_flashcards(
                module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES
            )
        assert isinstance(result, list)
        assert 1 <= len(result) <= 10

    def test_each_card_has_required_fields(self) -> None:
        """Every card contains question, answer, difficulty, and bloom_level."""
        mock_cls, _ = _make_mock_client(RICH_MOCK_FLASHCARDS)
        with patch("src.agents.flashcard_agent.anthropic.Anthropic", mock_cls):
            result = generate_flashcards(
                module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES
            )
        for card in result:
            assert "question" in card, f"Missing 'question' in {card}"
            assert "answer" in card, f"Missing 'answer' in {card}"
            assert "difficulty" in card, f"Missing 'difficulty' in {card}"
            assert "bloom_level" in card, f"Missing 'bloom_level' in {card}"

    def test_field_types_and_ranges(self) -> None:
        """question/answer are non-empty strings; difficulty is int 1-5; bloom_level is a string."""
        mock_cls, _ = _make_mock_client(RICH_MOCK_FLASHCARDS)
        with patch("src.agents.flashcard_agent.anthropic.Anthropic", mock_cls):
            result = generate_flashcards(
                module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES
            )
        for card in result:
            assert isinstance(card["question"], str) and card["question"].strip()
            assert isinstance(card["answer"], str) and card["answer"].strip()
            assert isinstance(card["difficulty"], int)
            assert 1 <= card["difficulty"] <= 5, f"difficulty out of range: {card['difficulty']}"
            assert isinstance(card["bloom_level"], str) and card["bloom_level"].strip()


# ---------------------------------------------------------------------------
# Test 2 — Empty input raises ValueError before any API call
# ---------------------------------------------------------------------------


class TestEmptyInput:
    """generate_flashcards raises ValueError when both inputs are empty."""

    def test_both_empty_raises_value_error(self) -> None:
        """Empty string inputs raise ValueError with a descriptive message."""
        mock_cls, _ = _make_mock_client(RICH_MOCK_FLASHCARDS)
        with patch("src.agents.flashcard_agent.anthropic.Anthropic", mock_cls):
            with pytest.raises(ValueError, match="At least one"):
                generate_flashcards(module_content="", student_notes="")

    def test_whitespace_only_raises_value_error(self) -> None:
        """Whitespace-only inputs are treated as empty."""
        mock_cls, _ = _make_mock_client(RICH_MOCK_FLASHCARDS)
        with patch("src.agents.flashcard_agent.anthropic.Anthropic", mock_cls):
            with pytest.raises(ValueError, match="At least one"):
                generate_flashcards(module_content="   ", student_notes="\t\n")

    def test_no_api_call_on_empty_input(self) -> None:
        """The Claude API must NOT be called when both inputs are empty."""
        mock_cls, mock_client = _make_mock_client(RICH_MOCK_FLASHCARDS)
        with patch("src.agents.flashcard_agent.anthropic.Anthropic", mock_cls):
            with pytest.raises(ValueError):
                generate_flashcards(module_content="", student_notes="")
        mock_client.messages.create.assert_not_called()


# ---------------------------------------------------------------------------
# Test 3 — Content integration: both sources appear in the user message
# ---------------------------------------------------------------------------


class TestContentIntegration:
    """Both module_content and student_notes are included in the message sent to Claude."""

    def test_both_sources_in_user_message(self) -> None:
        """The user-turn message forwarded to Claude contains text from both inputs."""
        mock_cls, mock_client = _make_mock_client(RICH_MOCK_FLASHCARDS)
        module_content = "Photosynthesis converts sunlight into glucose."
        student_notes = "Chlorophyll absorbs red and blue light wavelengths."

        with patch("src.agents.flashcard_agent.anthropic.Anthropic", mock_cls):
            generate_flashcards(module_content=module_content, student_notes=student_notes)

        call_kwargs = mock_client.messages.create.call_args.kwargs
        user_text = " ".join(
            m["content"] for m in call_kwargs["messages"] if m["role"] == "user"
        )
        assert "Photosynthesis" in user_text, (
            "module_content keyword not found in the user message sent to Claude"
        )
        assert "Chlorophyll" in user_text, (
            "student_notes keyword not found in the user message sent to Claude"
        )


# ---------------------------------------------------------------------------
# Test 4 — Bloom's variety: at least 3 distinct bloom_level values
# ---------------------------------------------------------------------------


class TestBloomsVariety:
    """Output contains at least 3 distinct bloom_level values."""

    def test_at_least_three_bloom_levels(self) -> None:
        """The result set spans ≥3 different Bloom's taxonomy levels."""
        mock_cls, _ = _make_mock_client(RICH_MOCK_FLASHCARDS)
        with patch("src.agents.flashcard_agent.anthropic.Anthropic", mock_cls):
            result = generate_flashcards(
                module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES
            )
        levels = {card["bloom_level"] for card in result}
        assert len(levels) >= 3, f"Expected ≥3 distinct bloom_levels, got: {levels}"


# ---------------------------------------------------------------------------
# Test 5 — Long input (5000+ chars) handled gracefully
# ---------------------------------------------------------------------------


class TestLongInput:
    """Agent handles combined inputs exceeding 5000 characters without raising."""

    def test_long_inputs_return_valid_flashcards(self) -> None:
        """5000-char inputs each return a valid non-empty list."""
        long_module = "Machine learning concepts. " * 200   # ~5400 chars
        long_notes = "Gradient descent details. " * 200     # ~5200 chars
        mock_cls, _ = _make_mock_client(RICH_MOCK_FLASHCARDS)
        with patch("src.agents.flashcard_agent.anthropic.Anthropic", mock_cls):
            result = generate_flashcards(module_content=long_module, student_notes=long_notes)
        assert isinstance(result, list)
        assert len(result) >= 1

    def test_long_input_no_exception_raised(self) -> None:
        """No exception is raised for maximally long inputs."""
        mock_cls, _ = _make_mock_client(RICH_MOCK_FLASHCARDS)
        with patch("src.agents.flashcard_agent.anthropic.Anthropic", mock_cls):
            try:
                generate_flashcards(
                    module_content="A" * 5000,
                    student_notes="B" * 5000,
                )
            except Exception as exc:  # noqa: BLE001
                pytest.fail(f"Unexpected exception for long input: {exc}")


# ---------------------------------------------------------------------------
# Test 6 — JSON parse failure raises ValueError
# ---------------------------------------------------------------------------


class TestJsonParseFailure:
    """Agent raises ValueError when Claude returns non-JSON text."""

    def test_non_json_response_raises_value_error(self) -> None:
        """A plain-text Claude response causes a ValueError with 'invalid JSON'."""
        mock_message = MagicMock()
        mock_message.content = [MagicMock()]
        mock_message.content[0].text = "Sorry, I cannot generate flashcards for that."

        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_message
        mock_cls = MagicMock(return_value=mock_client)

        with patch("src.agents.flashcard_agent.anthropic.Anthropic", mock_cls):
            with pytest.raises(ValueError, match="invalid JSON"):
                generate_flashcards(
                    module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES
                )


# ---------------------------------------------------------------------------
# Test 7 — Service integration: difficulty and bloom_level persisted in ORM
# ---------------------------------------------------------------------------


class TestServiceIntegration:
    """generate_and_store_flashcards maps difficulty and bloom_level into the Flashcard ORM."""

    def test_new_fields_in_stored_flashcards(
        self,
        client: TestClient,
        student_token: str,
        instructor_token: str,
    ) -> None:
        """POST /modules/{id}/flashcards stores and returns difficulty and bloom_level."""
        base_url = "/api/v1/modules"

        resp = client.post(
            base_url,
            json={"title": "Integration Test Module", "description": "Test description"},
            headers={"Authorization": f"Bearer {instructor_token}"},
        )
        assert resp.status_code == 201, resp.text
        module_id = resp.json()["id"]

        single_rich_card = [
            {
                "question": "What is AI?",
                "answer": "Artificial Intelligence.",
                "difficulty": 2,
                "bloom_level": "Remember",
            }
        ]

        with patch(
            "src.services.flashcard_service.generate_flashcards",
            return_value=single_rich_card,
        ):
            response = client.post(
                f"{base_url}/{module_id}/flashcards",
                headers={"Authorization": f"Bearer {student_token}"},
            )

        assert response.status_code == 201, response.text
        data = response.json()
        assert len(data) == 1
        assert data[0]["difficulty"] == 2
        assert data[0]["bloom_level"] == "Remember"
