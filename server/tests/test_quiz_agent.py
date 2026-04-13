"""
RED-phase tests for the QuizAgent generate_quiz function.

Tests are written BEFORE the implementation exists (pure TDD).
Running these against the current codebase must FAIL — that is the expected
RED state.

Covered scenarios
-----------------
1. Happy path       : dual inputs → dict with title, questions (5-15), difficulty_level
2. Empty input      : both empty strings → raises ValueError before any API call
3. Question types   : >=60% multiple_choice; >=1 short_answer; MC has exactly 4 options
4. Difficulty levels: Easy/Medium/Hard accepted; invalid level raises ValueError before API call
5. Long input       : 5000+ char inputs handled gracefully, returns valid dict
6. JSON failure     : Claude returns non-JSON → agent raises ValueError
7. Service mapping  : POST /modules/{id}/quizzes → stored quiz has all QuizResponse fields
"""

import json
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.agents.quiz_agent import generate_quiz

# ---------------------------------------------------------------------------
# Shared fixtures and helpers
# ---------------------------------------------------------------------------

MODULE_CONTENT = (
    "Neural networks are composed of layers of interconnected nodes. "
    "Each layer transforms its input using weights and activation functions. "
    "Deep learning uses many hidden layers to learn hierarchical representations. "
    "Convolutional neural networks are particularly effective for image recognition tasks."
)
STUDENT_NOTES = (
    "Activation functions introduce non-linearity — without them, the network "
    "is just a linear transform. ReLU is fast; sigmoid saturates at extremes. "
    "Backprop computes gradients layer by layer via the chain rule. "
    "Dropout randomly zeroes neurons during training to prevent overfitting."
)

MOCK_QUIZ = {
    "title": "Neural Networks and Deep Learning Quiz",
    "difficulty_level": "Medium",
    "questions": [
        {
            "id": 1,
            "text": "What is the primary purpose of an activation function?",
            "question_type": "multiple_choice",
            "options": [
                "To initialise weights",
                "To introduce non-linearity into the network",
                "To normalise input data",
                "To reduce model size",
            ],
            "correct_answer": "To introduce non-linearity into the network",
            "explanation": "Without activation functions, a neural network collapses to a linear model.",
        },
        {
            "id": 2,
            "text": "Which activation function is most commonly used in hidden layers of deep networks?",
            "question_type": "multiple_choice",
            "options": ["Sigmoid", "Tanh", "ReLU", "Softmax"],
            "correct_answer": "ReLU",
            "explanation": "ReLU is computationally efficient and avoids the vanishing gradient problem.",
        },
        {
            "id": 3,
            "text": "What does backpropagation compute?",
            "question_type": "multiple_choice",
            "options": [
                "Forward activations",
                "Gradients of the loss with respect to weights",
                "The number of layers needed",
                "The optimal learning rate",
            ],
            "correct_answer": "Gradients of the loss with respect to weights",
            "explanation": "Backprop uses the chain rule to compute gradients layer by layer.",
        },
        {
            "id": 4,
            "text": "What is the role of dropout in training neural networks?",
            "question_type": "multiple_choice",
            "options": [
                "To speed up forward passes",
                "To reduce the number of parameters",
                "To prevent overfitting by randomly zeroing neurons",
                "To increase learning rate automatically",
            ],
            "correct_answer": "To prevent overfitting by randomly zeroing neurons",
            "explanation": "Dropout acts as regularisation by preventing co-adaptation of neurons.",
        },
        {
            "id": 5,
            "text": "For which task are convolutional neural networks particularly effective?",
            "question_type": "multiple_choice",
            "options": [
                "Natural language processing",
                "Time-series forecasting",
                "Image recognition",
                "Reinforcement learning",
            ],
            "correct_answer": "Image recognition",
            "explanation": "CNNs exploit spatial locality via convolutional filters.",
        },
        {
            "id": 6,
            "text": "What problem does the sigmoid activation function suffer from in deep networks?",
            "question_type": "multiple_choice",
            "options": [
                "Exploding gradients",
                "Vanishing gradients",
                "Weight initialisation failure",
                "Excessive computation cost",
            ],
            "correct_answer": "Vanishing gradients",
            "explanation": "Sigmoid saturates near 0 and 1, causing gradients to shrink towards zero.",
        },
        {
            "id": 7,
            "text": "Explain how the chain rule is used in backpropagation.",
            "question_type": "short_answer",
            "options": None,
            "correct_answer": (
                "The chain rule decomposes the gradient of the loss with respect to "
                "early-layer weights into a product of local gradients, allowing efficient "
                "layer-by-layer computation."
            ),
            "explanation": (
                "Backpropagation is a direct application of the chain rule from calculus, "
                "propagating error signals backwards through the network."
            ),
        },
        {
            "id": 8,
            "text": "Describe the difference between underfitting and overfitting in neural network training.",
            "question_type": "short_answer",
            "options": None,
            "correct_answer": (
                "Underfitting occurs when the model is too simple to capture the training "
                "data patterns. Overfitting occurs when the model memorises training data "
                "and fails to generalise to new examples."
            ),
            "explanation": (
                "Regularisation techniques such as dropout, weight decay, and early stopping "
                "are used to combat overfitting."
            ),
        },
    ],
}


def _make_mock_client(quiz: dict) -> tuple[MagicMock, MagicMock]:
    """Return (mock_anthropic_class, mock_client) pre-wired with a JSON response.

    Args:
        quiz: Dict to serialise as the mocked Claude response.

    Returns:
        A tuple of (mock_anthropic_cls, mock_client) ready for use with patch().
    """
    mock_message = MagicMock()
    mock_message.content = [MagicMock()]
    mock_message.content[0].text = json.dumps(quiz)

    mock_client = MagicMock()
    mock_client.messages.create.return_value = mock_message

    mock_anthropic_cls = MagicMock(return_value=mock_client)
    return mock_anthropic_cls, mock_client


# ---------------------------------------------------------------------------
# Test 1 — Happy path
# ---------------------------------------------------------------------------


class TestHappyPath:
    """generate_quiz returns a well-formed dict for valid dual input."""

    def test_returns_dict(self) -> None:
        """Result is a dict."""
        mock_cls, _ = _make_mock_client(MOCK_QUIZ)
        with patch("src.agents.quiz_agent.anthropic.Anthropic", mock_cls):
            result = generate_quiz(
                module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES
            )
        assert isinstance(result, dict)

    def test_has_required_top_level_fields(self) -> None:
        """Dict contains title, questions, and difficulty_level."""
        mock_cls, _ = _make_mock_client(MOCK_QUIZ)
        with patch("src.agents.quiz_agent.anthropic.Anthropic", mock_cls):
            result = generate_quiz(
                module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES
            )
        assert "title" in result, "Missing 'title'"
        assert "questions" in result, "Missing 'questions'"
        assert "difficulty_level" in result, "Missing 'difficulty_level'"

    def test_questions_count_in_range(self) -> None:
        """questions list has between 5 and 15 items."""
        mock_cls, _ = _make_mock_client(MOCK_QUIZ)
        with patch("src.agents.quiz_agent.anthropic.Anthropic", mock_cls):
            result = generate_quiz(
                module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES
            )
        assert isinstance(result["questions"], list)
        assert 5 <= len(result["questions"]) <= 15, (
            f"Expected 5-15 questions, got {len(result['questions'])}"
        )

    def test_title_and_difficulty_types(self) -> None:
        """title is a non-empty string; difficulty_level is a valid level."""
        mock_cls, _ = _make_mock_client(MOCK_QUIZ)
        with patch("src.agents.quiz_agent.anthropic.Anthropic", mock_cls):
            result = generate_quiz(
                module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES
            )
        assert isinstance(result["title"], str) and result["title"].strip()
        assert result["difficulty_level"] in {"Easy", "Medium", "Hard"}


# ---------------------------------------------------------------------------
# Test 2 — Empty input raises ValueError before any API call
# ---------------------------------------------------------------------------


class TestEmptyInput:
    """generate_quiz raises ValueError when both inputs are empty."""

    def test_both_empty_raises_value_error(self) -> None:
        """Empty string inputs raise ValueError with a descriptive message."""
        mock_cls, _ = _make_mock_client(MOCK_QUIZ)
        with patch("src.agents.quiz_agent.anthropic.Anthropic", mock_cls):
            with pytest.raises(ValueError, match="At least one"):
                generate_quiz(module_content="", student_notes="")

    def test_whitespace_only_raises_value_error(self) -> None:
        """Whitespace-only inputs are treated as empty."""
        mock_cls, _ = _make_mock_client(MOCK_QUIZ)
        with patch("src.agents.quiz_agent.anthropic.Anthropic", mock_cls):
            with pytest.raises(ValueError, match="At least one"):
                generate_quiz(module_content="   ", student_notes="\t\n")

    def test_no_api_call_on_empty_input(self) -> None:
        """The Claude API must NOT be called when both inputs are empty."""
        mock_cls, mock_client = _make_mock_client(MOCK_QUIZ)
        with patch("src.agents.quiz_agent.anthropic.Anthropic", mock_cls):
            with pytest.raises(ValueError):
                generate_quiz(module_content="", student_notes="")
        mock_client.messages.create.assert_not_called()


# ---------------------------------------------------------------------------
# Test 3 — Question type constraints
# ---------------------------------------------------------------------------


class TestQuestionTypes:
    """Quiz contains correct mix of multiple_choice and short_answer questions."""

    def test_mc_ratio_at_least_60_percent(self) -> None:
        """At least 60% of questions are multiple_choice."""
        mock_cls, _ = _make_mock_client(MOCK_QUIZ)
        with patch("src.agents.quiz_agent.anthropic.Anthropic", mock_cls):
            result = generate_quiz(
                module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES
            )
        questions = result["questions"]
        mc_count = sum(1 for q in questions if q["question_type"] == "multiple_choice")
        ratio = mc_count / len(questions)
        assert ratio >= 0.6, f"Expected >=60% MC, got {ratio:.0%} ({mc_count}/{len(questions)})"

    def test_at_least_one_short_answer(self) -> None:
        """At least one question is short_answer."""
        mock_cls, _ = _make_mock_client(MOCK_QUIZ)
        with patch("src.agents.quiz_agent.anthropic.Anthropic", mock_cls):
            result = generate_quiz(
                module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES
            )
        sa_count = sum(1 for q in result["questions"] if q["question_type"] == "short_answer")
        assert sa_count >= 1, "Expected at least 1 short_answer question"

    def test_mc_questions_have_exactly_4_options(self) -> None:
        """Every multiple_choice question has exactly 4 options."""
        mock_cls, _ = _make_mock_client(MOCK_QUIZ)
        with patch("src.agents.quiz_agent.anthropic.Anthropic", mock_cls):
            result = generate_quiz(
                module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES
            )
        for q in result["questions"]:
            if q["question_type"] == "multiple_choice":
                assert isinstance(q.get("options"), list), (
                    f"MC question {q['id']} missing options list"
                )
                assert len(q["options"]) == 4, (
                    f"MC question {q['id']} has {len(q['options'])} options, expected 4"
                )

    def test_sa_questions_have_no_options(self) -> None:
        """short_answer questions have options as None or absent."""
        mock_cls, _ = _make_mock_client(MOCK_QUIZ)
        with patch("src.agents.quiz_agent.anthropic.Anthropic", mock_cls):
            result = generate_quiz(
                module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES
            )
        for q in result["questions"]:
            if q["question_type"] == "short_answer":
                assert q.get("options") is None, (
                    f"SA question {q['id']} should have options=None, got {q.get('options')}"
                )


# ---------------------------------------------------------------------------
# Test 4 — Difficulty levels
# ---------------------------------------------------------------------------


class TestDifficultyLevels:
    """generate_quiz accepts valid difficulty levels and rejects invalid ones."""

    def test_easy_level_accepted(self) -> None:
        """Level 'Easy' is accepted and passed through."""
        mock_quiz = {**MOCK_QUIZ, "difficulty_level": "Easy"}
        mock_cls, _ = _make_mock_client(mock_quiz)
        with patch("src.agents.quiz_agent.anthropic.Anthropic", mock_cls):
            result = generate_quiz(
                module_content=MODULE_CONTENT,
                student_notes=STUDENT_NOTES,
                difficulty_level="Easy",
            )
        assert result["difficulty_level"] == "Easy"

    def test_medium_level_accepted(self) -> None:
        """Level 'Medium' is accepted (also the default)."""
        mock_cls, _ = _make_mock_client(MOCK_QUIZ)
        with patch("src.agents.quiz_agent.anthropic.Anthropic", mock_cls):
            result = generate_quiz(
                module_content=MODULE_CONTENT,
                student_notes=STUDENT_NOTES,
                difficulty_level="Medium",
            )
        assert result["difficulty_level"] == "Medium"

    def test_hard_level_accepted(self) -> None:
        """Level 'Hard' is accepted."""
        mock_quiz = {**MOCK_QUIZ, "difficulty_level": "Hard"}
        mock_cls, _ = _make_mock_client(mock_quiz)
        with patch("src.agents.quiz_agent.anthropic.Anthropic", mock_cls):
            result = generate_quiz(
                module_content=MODULE_CONTENT,
                student_notes=STUDENT_NOTES,
                difficulty_level="Hard",
            )
        assert result["difficulty_level"] == "Hard"

    def test_invalid_level_raises_value_error_before_api(self) -> None:
        """An unrecognised difficulty level raises ValueError without calling Claude."""
        mock_cls, mock_client = _make_mock_client(MOCK_QUIZ)
        with patch("src.agents.quiz_agent.anthropic.Anthropic", mock_cls):
            with pytest.raises(ValueError, match="difficulty_level"):
                generate_quiz(
                    module_content=MODULE_CONTENT,
                    student_notes=STUDENT_NOTES,
                    difficulty_level="Expert",
                )
        mock_client.messages.create.assert_not_called()


# ---------------------------------------------------------------------------
# Test 5 — Long input handled gracefully
# ---------------------------------------------------------------------------


class TestLongInput:
    """Agent handles combined inputs exceeding 5000 characters without raising."""

    def test_long_inputs_return_valid_quiz(self) -> None:
        """5000-char inputs each return a valid dict with required fields."""
        long_module = "Neural network layer concepts. " * 170   # ~5270 chars
        long_notes = "Activation function details. " * 180       # ~5220 chars
        mock_cls, _ = _make_mock_client(MOCK_QUIZ)
        with patch("src.agents.quiz_agent.anthropic.Anthropic", mock_cls):
            result = generate_quiz(module_content=long_module, student_notes=long_notes)
        assert isinstance(result, dict)
        assert "questions" in result

    def test_long_input_no_exception_raised(self) -> None:
        """No exception is raised for maximally long inputs."""
        mock_cls, _ = _make_mock_client(MOCK_QUIZ)
        with patch("src.agents.quiz_agent.anthropic.Anthropic", mock_cls):
            try:
                generate_quiz(
                    module_content="A" * 5000,
                    student_notes="B" * 5000,
                )
            except Exception as exc:  # noqa: BLE001
                pytest.fail(f"Unexpected exception for long input: {exc}")


# ---------------------------------------------------------------------------
# Test 6 — JSON parse failure raises ValueError
# ---------------------------------------------------------------------------


class TestValidation:
    """_validate_quiz and _validate_question raise ValueError for malformed Claude responses."""

    def _mock_for(self, bad_quiz: dict) -> MagicMock:
        """Return a mock_cls that makes Claude return bad_quiz as JSON."""
        mock_cls, _ = _make_mock_client(bad_quiz)
        return mock_cls

    def test_response_is_list_not_dict(self) -> None:
        """Claude returns a JSON array instead of object → ValueError."""
        mock_cls, _ = _make_mock_client([])  # list, not dict
        with patch("src.agents.quiz_agent.anthropic.Anthropic", mock_cls):
            with pytest.raises(ValueError, match="JSON object"):
                generate_quiz(module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES)

    def test_missing_title_field(self) -> None:
        """Response missing 'title' → ValueError."""
        bad = {k: v for k, v in MOCK_QUIZ.items() if k != "title"}
        with patch("src.agents.quiz_agent.anthropic.Anthropic", self._mock_for(bad)):
            with pytest.raises(ValueError, match="title"):
                generate_quiz(module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES)

    def test_empty_title(self) -> None:
        """Response with empty title string → ValueError."""
        bad = {**MOCK_QUIZ, "title": "   "}
        with patch("src.agents.quiz_agent.anthropic.Anthropic", self._mock_for(bad)):
            with pytest.raises(ValueError, match="title"):
                generate_quiz(module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES)

    def test_invalid_difficulty_in_response(self) -> None:
        """Response with unrecognised difficulty_level → ValueError."""
        bad = {**MOCK_QUIZ, "difficulty_level": "Extreme"}
        with patch("src.agents.quiz_agent.anthropic.Anthropic", self._mock_for(bad)):
            with pytest.raises(ValueError, match="difficulty_level"):
                generate_quiz(module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES)

    def test_questions_not_a_list(self) -> None:
        """Response with questions as a string → ValueError."""
        bad = {**MOCK_QUIZ, "questions": "not a list"}
        with patch("src.agents.quiz_agent.anthropic.Anthropic", self._mock_for(bad)):
            with pytest.raises(ValueError, match="questions"):
                generate_quiz(module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES)

    def test_too_few_questions(self) -> None:
        """Response with fewer than 5 questions → ValueError."""
        bad = {**MOCK_QUIZ, "questions": MOCK_QUIZ["questions"][:2]}
        with patch("src.agents.quiz_agent.anthropic.Anthropic", self._mock_for(bad)):
            with pytest.raises(ValueError, match="5"):
                generate_quiz(module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES)

    def test_mc_ratio_below_60_percent(self) -> None:
        """Response where less than 60% are MC → ValueError."""
        # 2 SA out of 5 total = only 60% MC exactly — use 3 SA out of 5
        all_sa = [
            {**q, "question_type": "short_answer", "options": None}
            for q in MOCK_QUIZ["questions"][:5]
        ]
        bad = {**MOCK_QUIZ, "questions": all_sa}
        with patch("src.agents.quiz_agent.anthropic.Anthropic", self._mock_for(bad)):
            with pytest.raises(ValueError, match="60%"):
                generate_quiz(module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES)

    def test_no_short_answer_questions(self) -> None:
        """Response with all MC questions (no SA) → ValueError."""
        all_mc = [
            {
                **MOCK_QUIZ["questions"][i % 6],  # use one of the 6 MC questions
                "id": i + 1,
                "question_type": "multiple_choice",
                "options": ["A", "B", "C", "D"],
            }
            for i in range(6)
        ]
        bad = {**MOCK_QUIZ, "questions": all_mc}
        with patch("src.agents.quiz_agent.anthropic.Anthropic", self._mock_for(bad)):
            with pytest.raises(ValueError, match="short_answer"):
                generate_quiz(module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES)

    def test_question_missing_required_field(self) -> None:
        """A question missing 'text' → ValueError."""
        bad_q = {k: v for k, v in MOCK_QUIZ["questions"][0].items() if k != "text"}
        bad = {**MOCK_QUIZ, "questions": [bad_q] + MOCK_QUIZ["questions"][1:]}
        with patch("src.agents.quiz_agent.anthropic.Anthropic", self._mock_for(bad)):
            with pytest.raises(ValueError, match="text"):
                generate_quiz(module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES)

    def test_question_empty_correct_answer(self) -> None:
        """A question with empty correct_answer → ValueError."""
        bad_q = {**MOCK_QUIZ["questions"][0], "correct_answer": ""}
        bad = {**MOCK_QUIZ, "questions": [bad_q] + MOCK_QUIZ["questions"][1:]}
        with patch("src.agents.quiz_agent.anthropic.Anthropic", self._mock_for(bad)):
            with pytest.raises(ValueError, match="correct_answer"):
                generate_quiz(module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES)

    def test_question_empty_explanation(self) -> None:
        """A question with empty explanation → ValueError."""
        bad_q = {**MOCK_QUIZ["questions"][0], "explanation": "   "}
        bad = {**MOCK_QUIZ, "questions": [bad_q] + MOCK_QUIZ["questions"][1:]}
        with patch("src.agents.quiz_agent.anthropic.Anthropic", self._mock_for(bad)):
            with pytest.raises(ValueError, match="explanation"):
                generate_quiz(module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES)

    def test_question_invalid_type(self) -> None:
        """A question with unrecognised question_type → ValueError."""
        bad_q = {**MOCK_QUIZ["questions"][0], "question_type": "true_false"}
        bad = {**MOCK_QUIZ, "questions": [bad_q] + MOCK_QUIZ["questions"][1:]}
        with patch("src.agents.quiz_agent.anthropic.Anthropic", self._mock_for(bad)):
            with pytest.raises(ValueError, match="question_type"):
                generate_quiz(module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES)

    def test_mc_question_wrong_options_count(self) -> None:
        """An MC question with only 3 options → ValueError."""
        bad_q = {**MOCK_QUIZ["questions"][0], "options": ["A", "B", "C"]}
        bad = {**MOCK_QUIZ, "questions": [bad_q] + MOCK_QUIZ["questions"][1:]}
        with patch("src.agents.quiz_agent.anthropic.Anthropic", self._mock_for(bad)):
            with pytest.raises(ValueError, match="4 options"):
                generate_quiz(module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES)

    def test_mc_question_empty_option_string(self) -> None:
        """An MC question with a blank option string → ValueError."""
        bad_q = {**MOCK_QUIZ["questions"][0], "options": ["A", "B", "C", ""]}
        bad = {**MOCK_QUIZ, "questions": [bad_q] + MOCK_QUIZ["questions"][1:]}
        with patch("src.agents.quiz_agent.anthropic.Anthropic", self._mock_for(bad)):
            with pytest.raises(ValueError, match="non-empty string"):
                generate_quiz(module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES)

    def test_sa_question_with_options(self) -> None:
        """A short_answer question that has a non-None options list → ValueError."""
        bad_q = {**MOCK_QUIZ["questions"][6], "options": ["A", "B", "C", "D"]}
        bad = {**MOCK_QUIZ, "questions": MOCK_QUIZ["questions"][:6] + [bad_q]}
        with patch("src.agents.quiz_agent.anthropic.Anthropic", self._mock_for(bad)):
            with pytest.raises(ValueError, match="options=None"):
                generate_quiz(module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES)


class TestJsonParseFailure:
    """Agent raises ValueError when Claude returns non-JSON text."""

    def test_non_json_response_raises_value_error(self) -> None:
        """A plain-text Claude response causes a ValueError with 'invalid JSON'."""
        mock_message = MagicMock()
        mock_message.content = [MagicMock()]
        mock_message.content[0].text = "I cannot generate a quiz for that content."

        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_message
        mock_cls = MagicMock(return_value=mock_client)

        with patch("src.agents.quiz_agent.anthropic.Anthropic", mock_cls):
            with pytest.raises(ValueError, match="invalid JSON"):
                generate_quiz(
                    module_content=MODULE_CONTENT, student_notes=STUDENT_NOTES
                )


# ---------------------------------------------------------------------------
# Test 7 — Service integration: all QuizResponse fields returned via HTTP
# ---------------------------------------------------------------------------


class TestServiceIntegration:
    """POST /modules/{id}/quizzes stores and returns all QuizResponse fields."""

    def test_quiz_endpoint_returns_201_with_all_fields(
        self,
        client: TestClient,
        student_token: str,
        instructor_token: str,
    ) -> None:
        """POST endpoint returns 201 with id, title, difficulty_level, questions list."""
        base_url = "/api/v1/modules"

        resp = client.post(
            base_url,
            json={"title": "Quiz Integration Module", "description": "Test description"},
            headers={"Authorization": f"Bearer {instructor_token}"},
        )
        assert resp.status_code == 201, resp.text
        module_id = resp.json()["id"]

        minimal_quiz = {
            "title": "Test Quiz",
            "difficulty_level": "Easy",
            "questions": [
                {
                    "id": 1,
                    "text": "What is AI?",
                    "question_type": "multiple_choice",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": "Option A",
                    "explanation": "AI stands for Artificial Intelligence.",
                },
                {
                    "id": 2,
                    "text": "Define machine learning.",
                    "question_type": "short_answer",
                    "options": None,
                    "correct_answer": "ML is a subset of AI that learns from data.",
                    "explanation": "ML algorithms improve through experience.",
                },
                {
                    "id": 3,
                    "text": "What does GPU stand for?",
                    "question_type": "multiple_choice",
                    "options": [
                        "General Processing Unit",
                        "Graphics Processing Unit",
                        "Global Processing Unit",
                        "Graphic Parallel Unit",
                    ],
                    "correct_answer": "Graphics Processing Unit",
                    "explanation": "GPUs are used for parallel computations.",
                },
                {
                    "id": 4,
                    "text": "Which is a supervised learning algorithm?",
                    "question_type": "multiple_choice",
                    "options": ["K-means", "PCA", "Linear Regression", "DBSCAN"],
                    "correct_answer": "Linear Regression",
                    "explanation": "Linear regression uses labelled training data.",
                },
                {
                    "id": 5,
                    "text": "What is overfitting?",
                    "question_type": "multiple_choice",
                    "options": [
                        "Model too simple",
                        "Model memorises training data",
                        "Model has too few parameters",
                        "Model trains too slowly",
                    ],
                    "correct_answer": "Model memorises training data",
                    "explanation": "Overfitting means poor generalisation to new data.",
                },
            ],
        }

        with patch(
            "src.services.quiz_service.generate_quiz",
            return_value=minimal_quiz,
        ):
            response = client.post(
                f"{base_url}/{module_id}/quizzes",
                json={"difficulty_level": "Easy"},
                headers={"Authorization": f"Bearer {student_token}"},
            )

        assert response.status_code == 201, response.text
        data = response.json()
        assert data["title"] == "Test Quiz"
        assert data["difficulty_level"] == "Easy"
        assert data["module_id"] == module_id
        assert "student_id" in data
        assert "id" in data
        assert "created_at" in data
        assert isinstance(data["questions"], list)
        assert len(data["questions"]) == 5
        first_q = data["questions"][0]
        assert "id" in first_q
        assert "text" in first_q
        assert "question_type" in first_q
        assert "correct_answer" in first_q
        assert "explanation" in first_q
