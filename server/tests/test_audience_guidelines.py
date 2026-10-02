"""Tests for instructor audience guidelines in agent system prompts.

Instructors describe their class in ``audience_context`` (course level, and
optionally module level). These tests check that the text reaches the system
prompt of the quiz, flashcard and summary agents, and that generation without
guidelines sends the base prompt unchanged.
"""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.agents.flashcard_agent import generate_flashcards
from src.agents.prompts import flashcard_prompt, quiz_prompt, summary_prompt
from src.agents.prompts.audience import (
    MAX_AUDIENCE_CHARS,
    MAX_GUIDELINES_CHARS,
    combine_audience_context,
    with_audience_guidelines,
)
from src.agents.quiz_agent import generate_quiz
from src.agents.summary_agent import generate_summary
from tests.test_flashcard_agent import RICH_MOCK_FLASHCARDS
from tests.test_quiz_agent import MOCK_QUIZ
from tests.test_summary_agent import MOCK_SUMMARY

GUIDELINE = "Some students have lost a parent. Avoid examples that assume two parents at home."


def _mock_anthropic(tool_input: object) -> tuple[MagicMock, MagicMock]:
    """Return (mock_anthropic_cls, mock_client) whose reply is one tool_use block."""
    tool_use = MagicMock()
    tool_use.type = "tool_use"
    tool_use.input = tool_input
    message = MagicMock()
    message.content = [tool_use]
    client = MagicMock()
    client.messages.create.return_value = message
    return MagicMock(return_value=client), client


class TestWithAudienceGuidelines:
    """Unit tests for the system-prompt builder."""

    def test_empty_guidelines_return_base_prompt(self) -> None:
        assert with_audience_guidelines("BASE", "") == "BASE"
        assert with_audience_guidelines("BASE", "   \n ") == "BASE"

    def test_guidelines_are_appended_after_base_prompt(self) -> None:
        prompt = with_audience_guidelines("BASE", GUIDELINE)
        assert prompt.startswith("BASE")
        assert GUIDELINE in prompt
        assert "Audience guidelines" in prompt

    def test_guidelines_do_not_override_output_rules(self) -> None:
        prompt = with_audience_guidelines("BASE", GUIDELINE)
        assert "never change the output format" in prompt

    def test_long_guidelines_are_truncated(self) -> None:
        prompt = with_audience_guidelines("BASE", "x" * (MAX_GUIDELINES_CHARS + 500))
        assert "x" * MAX_GUIDELINES_CHARS in prompt
        assert "x" * (MAX_GUIDELINES_CHARS + 1) not in prompt


class TestCombineAudienceContext:
    """Course-level and module-level text are merged in that order."""

    def test_both_levels(self) -> None:
        text = combine_audience_context("Girls' school.", "Use women engineers as examples.")
        assert text.index("Girls' school.") < text.index("Use women engineers as examples.")

    def test_each_level_is_truncated(self) -> None:
        text = combine_audience_context("c" * 1500, "m" * 1500)
        assert text.count("c") == MAX_AUDIENCE_CHARS
        assert text.count("m") == MAX_AUDIENCE_CHARS
        assert len(text) <= MAX_GUIDELINES_CHARS

    def test_missing_levels(self) -> None:
        assert combine_audience_context(None, None) == ""
        assert combine_audience_context("  ", None) == ""
        assert combine_audience_context(None, "Module only") == "Module: Module only"
        assert combine_audience_context("Class only", "") == "Class: Class only"


@pytest.mark.parametrize(
    ("patch_target", "call", "tool_input", "base_prompt"),
    [
        (
            "src.agents.quiz_agent.anthropic.Anthropic",
            lambda ctx: generate_quiz(
                "Course text", "", "Medium", len(MOCK_QUIZ["questions"]), audience_context=ctx
            ),
            MOCK_QUIZ,
            quiz_prompt.SYSTEM_PROMPT,
        ),
        (
            "src.agents.flashcard_agent.anthropic.Anthropic",
            lambda ctx: generate_flashcards("Course text", "", audience_context=ctx),
            {"flashcards": RICH_MOCK_FLASHCARDS},
            flashcard_prompt.SYSTEM_PROMPT,
        ),
        (
            "src.agents.summary_agent.anthropic.Anthropic",
            lambda ctx: generate_summary("Course text", "", "Standard", audience_context=ctx),
            MOCK_SUMMARY,
            summary_prompt.SYSTEM_PROMPT,
        ),
    ],
    ids=["quiz", "flashcard", "summary"],
)
class TestAgentsSendGuidelines:
    """Each agent puts the instructor's guidelines into the system prompt."""

    def test_guidelines_in_system_prompt(self, patch_target, call, tool_input, base_prompt) -> None:
        mock_cls, client = _mock_anthropic(tool_input)
        with patch(patch_target, mock_cls):
            call(GUIDELINE)
        system = client.messages.create.call_args.kwargs["system"]
        assert system.startswith(base_prompt)
        assert GUIDELINE in system

    def test_no_guidelines_sends_base_prompt(self, patch_target, call, tool_input, base_prompt):
        mock_cls, client = _mock_anthropic(tool_input)
        with patch(patch_target, mock_cls):
            call("")
        assert client.messages.create.call_args.kwargs["system"] == base_prompt


def _auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _create_course_module(client: TestClient, instructor_token: str, suffix: str) -> int:
    """Create a course with class-level guidelines and a module with its own; return module id."""
    course = client.post(
        "/api/v1/courses",
        json={"title": f"Audience Course {suffix}", "audience_context": "Girls' school."},
        headers=_auth(instructor_token),
    )
    assert course.status_code == 201, course.text
    module = client.post(
        "/api/v1/modules",
        json={
            "title": f"Audience Module {suffix}",
            "description": "Forces and motion.",
            "audience_context": "Use women engineers as examples.",
            "course_id": course.json()["id"],
        },
        headers=_auth(instructor_token),
    )
    assert module.status_code == 201, module.text
    return module.json()["id"]


class TestServicesPassGuidelines:
    """Generation endpoints pass course and module guidelines to the agents."""

    def _assert_both_levels(self, mock_agent: MagicMock) -> None:
        ctx = mock_agent.call_args.kwargs["audience_context"]
        assert "Girls' school." in ctx
        assert "Use women engineers as examples." in ctx

    def test_quiz(self, client: TestClient, instructor_token: str, student_token: str) -> None:
        module_id = _create_course_module(client, instructor_token, "quiz")
        with patch("src.services.quiz_service.generate_quiz", return_value=MOCK_QUIZ) as agent:
            res = client.post(f"/api/v1/modules/{module_id}/quizzes", headers=_auth(student_token))
        assert res.status_code == 201, res.text
        self._assert_both_levels(agent)

    def test_flashcards(
        self, client: TestClient, instructor_token: str, student_token: str
    ) -> None:
        module_id = _create_course_module(client, instructor_token, "flashcards")
        with patch(
            "src.services.flashcard_service.generate_flashcards",
            return_value=RICH_MOCK_FLASHCARDS,
        ) as agent:
            res = client.post(
                f"/api/v1/modules/{module_id}/flashcards", headers=_auth(student_token)
            )
        assert res.status_code == 201, res.text
        self._assert_both_levels(agent)

    def test_summary(self, client: TestClient, instructor_token: str, student_token: str) -> None:
        module_id = _create_course_module(client, instructor_token, "summary")
        with patch(
            "src.services.summary_service.generate_summary", return_value=MOCK_SUMMARY
        ) as agent:
            res = client.post(
                f"/api/v1/modules/{module_id}/summaries", headers=_auth(student_token)
            )
        assert res.status_code == 201, res.text
        self._assert_both_levels(agent)
