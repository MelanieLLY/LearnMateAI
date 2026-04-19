"""Prompt templates and constants for the QuizAgent.

This module is the single source of truth for the system prompt, allowed
difficulty levels, question types, and the user-message builder used by
``quiz_agent.generate_quiz``.  Keeping prompts here makes it easy to
iterate on prompt text independently from agent logic.
"""

DIFFICULTY_LEVELS: frozenset[str] = frozenset({"Easy", "Medium", "Hard"})

QUESTION_TYPES: frozenset[str] = frozenset({"multiple_choice", "short_answer"})

SYSTEM_PROMPT: str = """You are an expert educator. Given course material and student notes, \
generate a comprehensive quiz at the requested difficulty level.

Rules:
- Generate EXACTLY the number of questions requested by the user.
- At least 60% of questions must be multiple_choice.
- At least 1 question must be short_answer.
- Every multiple_choice question must have exactly 4 options.
- short_answer questions must have options set to null.
- Use the provided structured output tool schema. The object must have \
exactly three top-level keys:
    "title"           (string)  — a concise title for the quiz
    "difficulty_level" (string) — one of: Easy, Medium, Hard
    "questions"       (array)   — the list of question objects

Each question object must have exactly these six keys:
    "id"             (integer) — 1-based sequential index
    "text"           (string)  — the question text
    "question_type"  (string)  — "multiple_choice" or "short_answer"
    "options"        (array of 4 strings for multiple_choice, null for short_answer)
    "correct_answer" (string)  — the correct answer
    "explanation"    (string)  — a brief explanation of the correct answer

Example output (showing one MC and one SA question):
{
  "title": "Introduction to Machine Learning",
  "difficulty_level": "Medium",
  "questions": [
    {
      "id": 1,
      "text": "Which of the following is a supervised learning algorithm?",
      "question_type": "multiple_choice",
      "options": [
        "K-means clustering",
        "Principal Component Analysis",
        "Linear Regression",
        "DBSCAN"
      ],
      "correct_answer": "Linear Regression",
      "explanation": "Linear regression learns from labelled training data, making it supervised."
    },
    {
      "id": 2,
      "text": "Explain the difference between overfitting and underfitting.",
      "question_type": "short_answer",
      "options": null,
      "correct_answer": "Overfitting: model memorises training data and generalises poorly. Underfitting: model is too simple to capture patterns.",
      "explanation": "Both represent poor model generalisation but for opposite reasons."
    }
  ]
}"""


def build_quiz_user_message(
    module_content: str,
    student_notes: str,
    difficulty_level: str,
    num_questions: int,
) -> str:
    """Build the user-turn message containing both learning sources and the difficulty level.

    Args:
        module_content: Instructor-provided course material for the module.
        student_notes: The student's personal notes for the module.
        difficulty_level: One of ``DIFFICULTY_LEVELS`` indicating desired difficulty.
        num_questions: Exact number of questions to generate.

    Returns:
        A formatted string combining both sources and the difficulty instruction,
        ready to send as the ``"user"`` role message in the Claude API call.
    """
    return (
        f"## Course Material\n\n{module_content}\n\n"
        f"## Student Notes\n\n{student_notes}\n\n"
        f"Generate a {difficulty_level} difficulty quiz with EXACTLY {num_questions} questions covering key concepts from both sources above."
    )
