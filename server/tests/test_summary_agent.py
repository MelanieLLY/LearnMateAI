"""
RED-phase tests for the SummaryAgent generate_summary function.

Tests are written BEFORE the implementation exists (pure TDD).
Running these against the current codebase must FAIL — that is the expected
RED state.

Covered scenarios
-----------------
1. Happy path       : dual inputs → dict with title, content, word_count, summary_level
2. Empty input      : both empty strings → raises ValueError before any API call
3. Content integration: user message sent to Claude contains both module_content and student_notes
4. Summary levels   : Brief/Standard/Detailed accepted; invalid level raises ValueError
5. Long input       : 5000+ char inputs handled gracefully, returns valid dict
6. JSON failure     : Claude returns non-JSON → agent raises ValueError
7. Service mapping  : POST /modules/{id}/summaries → stored summary has all new fields
"""

import json
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.agents.summary_agent import generate_summary

# ---------------------------------------------------------------------------
# Shared fixtures and helpers
# ---------------------------------------------------------------------------

MODULE_CONTENT = (
    "Neural networks are composed of layers of interconnected nodes. "
    "Each layer transforms its input using weights and activation functions. "
    "Deep learning uses many hidden layers to learn hierarchical representations."
)
STUDENT_NOTES = (
    "Activation functions introduce non-linearity — without them, the network "
    "is just a linear transform. ReLU is fast; sigmoid saturates at extremes. "
    "Backprop computes gradients layer by layer via the chain rule."
)

MOCK_SUMMARY = {
    "title": "Introduction to Neural Networks",
    "content": (
        "Neural networks consist of interconnected layers that transform inputs "
        "using weights and activation functions such as ReLU or sigmoid. "
        "Deep learning leverages many hidden layers to extract hierarchical features. "
        "Backpropagation enables efficient gradient computation via the chain rule, "
        "allowing the network to learn from labelled data."
    ),
    "word_count": 52,
    "summary_level": "Standard",
}


def _make_mock_client(summary: dict) -> tuple[MagicMock, MagicMock]:
    """Return (mock_anthropic_class, mock_client) pre-wired with a JSON response.

    Args:
        summary: Dict to serialise as the mocked Claude response.

    Returns:
        A tuple of (mock_anthropic_cls, mock_client) ready for use with patch().
    """
    mock_message = MagicMock()
    mock_message.content = [MagicMock()]
    mock_message.content[0].text = json.dumps(summary)

    mock_client = MagicMock()
    mock_client.messages.create.return_value = mock_message

    mock_anthropic_cls = MagicMock(return_value=mock_client)
    return mock_anthropic_cls, mock_client


# ---------------------------------------------------------------------------
# Test 1 — Happy path
# ---------------------------------------------------------------------------


class TestHappyPath:
    """generate_summary returns a well-formed dict for valid dual input."""

    def test_returns_dict(self) -> None:
        """Result is a dict."""
        mock_cls, _ = _make_mock_client(MOCK_SUMMARY)
        with patch("src.agents.summary_agent.anthropic.Anthropic", mock_cls):
            result = generate_summary(
                module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES
            )
        assert isinstance(result, dict)

    def test_has_required_fields(self) -> None:
        """Dict contains title, content, word_count, and summary_level."""
        mock_cls, _ = _make_mock_client(MOCK_SUMMARY)
        with patch("src.agents.summary_agent.anthropic.Anthropic", mock_cls):
            result = generate_summary(
                module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES
            )
        assert "title" in result, "Missing 'title'"
        assert "content" in result, "Missing 'content'"
        assert "word_count" in result, "Missing 'word_count'"
        assert "summary_level" in result, "Missing 'summary_level'"

    def test_field_types_and_values(self) -> None:
        """Fields have correct types and meaningful values."""
        mock_cls, _ = _make_mock_client(MOCK_SUMMARY)
        with patch("src.agents.summary_agent.anthropic.Anthropic", mock_cls):
            result = generate_summary(
                module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES
            )
        assert isinstance(result["title"], str) and result["title"].strip()
        assert isinstance(result["content"], str) and result["content"].strip()
        assert isinstance(result["word_count"], int) and result["word_count"] > 0
        assert result["summary_level"] in {"Brief", "Standard", "Detailed"}


# ---------------------------------------------------------------------------
# Test 2 — Empty input raises ValueError before any API call
# ---------------------------------------------------------------------------


class TestEmptyInput:
    """generate_summary raises ValueError when both inputs are empty."""

    def test_both_empty_raises_value_error(self) -> None:
        """Empty string inputs raise ValueError with a descriptive message."""
        mock_cls, _ = _make_mock_client(MOCK_SUMMARY)
        with patch("src.agents.summary_agent.anthropic.Anthropic", mock_cls):
            with pytest.raises(ValueError, match="At least one"):
                generate_summary(module_content="", student_notes="")

    def test_whitespace_only_raises_value_error(self) -> None:
        """Whitespace-only inputs are treated as empty."""
        mock_cls, _ = _make_mock_client(MOCK_SUMMARY)
        with patch("src.agents.summary_agent.anthropic.Anthropic", mock_cls):
            with pytest.raises(ValueError, match="At least one"):
                generate_summary(module_content="   ", student_notes="\t\n")

    def test_no_api_call_on_empty_input(self) -> None:
        """The Claude API must NOT be called when both inputs are empty."""
        mock_cls, mock_client = _make_mock_client(MOCK_SUMMARY)
        with patch("src.agents.summary_agent.anthropic.Anthropic", mock_cls):
            with pytest.raises(ValueError):
                generate_summary(module_content="", student_notes="")
        mock_client.messages.create.assert_not_called()


# ---------------------------------------------------------------------------
# Test 3 — Content integration: both sources appear in the user message
# ---------------------------------------------------------------------------


class TestContentIntegration:
    """Both module_content and student_notes are included in the message sent to Claude."""

    def test_both_sources_in_user_message(self) -> None:
        """The user-turn message forwarded to Claude contains text from both inputs."""
        mock_cls, mock_client = _make_mock_client(MOCK_SUMMARY)
        module_content = "Photosynthesis converts sunlight into glucose."
        student_notes = "Chlorophyll absorbs red and blue light wavelengths."

        with patch("src.agents.summary_agent.anthropic.Anthropic", mock_cls):
            generate_summary(module_content=module_content, student_notes=student_notes)

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
# Test 4 — Summary levels
# ---------------------------------------------------------------------------


class TestSummaryLevels:
    """generate_summary accepts valid levels and rejects invalid ones."""

    def test_brief_level_accepted(self) -> None:
        """Level 'Brief' is accepted and passed through."""
        mock_summary = {**MOCK_SUMMARY, "summary_level": "Brief"}
        mock_cls, _ = _make_mock_client(mock_summary)
        with patch("src.agents.summary_agent.anthropic.Anthropic", mock_cls):
            result = generate_summary(
                module_content=MODULE_CONTENT,
                student_notes=STUDENT_NOTES,
                summary_level="Brief",
            )
        assert result["summary_level"] == "Brief"

    def test_standard_level_accepted(self) -> None:
        """Level 'Standard' is accepted (also the default)."""
        mock_cls, _ = _make_mock_client(MOCK_SUMMARY)
        with patch("src.agents.summary_agent.anthropic.Anthropic", mock_cls):
            result = generate_summary(
                module_content=MODULE_CONTENT,
                student_notes=STUDENT_NOTES,
                summary_level="Standard",
            )
        assert result["summary_level"] == "Standard"

    def test_detailed_level_accepted(self) -> None:
        """Level 'Detailed' is accepted."""
        mock_summary = {**MOCK_SUMMARY, "summary_level": "Detailed"}
        mock_cls, _ = _make_mock_client(mock_summary)
        with patch("src.agents.summary_agent.anthropic.Anthropic", mock_cls):
            result = generate_summary(
                module_content=MODULE_CONTENT,
                student_notes=STUDENT_NOTES,
                summary_level="Detailed",
            )
        assert result["summary_level"] == "Detailed"

    def test_invalid_level_raises_value_error(self) -> None:
        """An unrecognised level raises ValueError before any API call."""
        mock_cls, mock_client = _make_mock_client(MOCK_SUMMARY)
        with patch("src.agents.summary_agent.anthropic.Anthropic", mock_cls):
            with pytest.raises(ValueError, match="summary_level"):
                generate_summary(
                    module_content=MODULE_CONTENT,
                    student_notes=STUDENT_NOTES,
                    summary_level="Expert",
                )
        mock_client.messages.create.assert_not_called()


# ---------------------------------------------------------------------------
# Test 5 — Long input (5000+ chars) handled gracefully
# ---------------------------------------------------------------------------


class TestLongInput:
    """Agent handles combined inputs exceeding 5000 characters without raising."""

    def test_long_inputs_return_valid_summary(self) -> None:
        """5000-char inputs each return a valid dict."""
        long_module = "Neural networks learn representations. " * 150   # ~5700 chars
        long_notes = "Activation functions are critical. " * 150         # ~5250 chars
        mock_cls, _ = _make_mock_client(MOCK_SUMMARY)
        with patch("src.agents.summary_agent.anthropic.Anthropic", mock_cls):
            result = generate_summary(module_content=long_module, student_notes=long_notes)
        assert isinstance(result, dict)
        assert "title" in result

    def test_long_input_no_exception_raised(self) -> None:
        """No exception is raised for maximally long inputs."""
        mock_cls, _ = _make_mock_client(MOCK_SUMMARY)
        with patch("src.agents.summary_agent.anthropic.Anthropic", mock_cls):
            try:
                generate_summary(
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
        mock_message.content[0].text = "I cannot summarise that content."

        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_message
        mock_cls = MagicMock(return_value=mock_client)

        with patch("src.agents.summary_agent.anthropic.Anthropic", mock_cls):
            with pytest.raises(ValueError, match="invalid JSON"):
                generate_summary(
                    module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES
                )


# ---------------------------------------------------------------------------
# Test 7 — Service integration: all fields persisted and returned via HTTP
# ---------------------------------------------------------------------------


class TestServiceIntegration:
    """POST /modules/{id}/summaries stores and returns all summary fields."""

    def test_summary_endpoint_returns_all_fields(
        self,
        client: TestClient,
        student_token: str,
        instructor_token: str,
    ) -> None:
        """POST endpoint returns 201 with title, content, word_count, summary_level."""
        base_url = "/api/v1/modules"

        resp = client.post(
            base_url,
            json={"title": "Summary Integration Module", "description": "Test description"},
            headers={"Authorization": f"Bearer {instructor_token}"},
        )
        assert resp.status_code == 201, resp.text
        module_id = resp.json()["id"]

        # The service recomputes word_count = len(content.split()) at write time.
        # "This is the summary content for testing purposes." → 8 words.
        with patch(
            "src.services.summary_service.generate_summary",
            return_value={
                "title": "Test Summary",
                "content": "This is the summary content for testing purposes.",
                "word_count": 8,
                "summary_level": "Brief",
            },
        ):
            response = client.post(
                f"{base_url}/{module_id}/summaries",
                json={"summary_level": "Brief"},
                headers={"Authorization": f"Bearer {student_token}"},
            )

        assert response.status_code == 201, response.text
        data = response.json()
        assert data["title"] == "Test Summary"
        assert data["content"] == "This is the summary content for testing purposes."
        assert data["word_count"] == 8
        assert data["summary_level"] == "Brief"
        assert data["module_id"] == module_id
        assert "student_id" in data
        assert "id" in data
        assert "created_at" in data
