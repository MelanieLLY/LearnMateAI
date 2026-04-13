"""Prompt templates and constants for the FlashcardAgent.

This module is the single source of truth for the system prompt, the allowed
Bloom's taxonomy levels, and the user-message builder used by
``flashcard_agent.generate_flashcards``.  Keeping prompts here makes it easy
to iterate on the prompt independently from the agent logic.
"""

BLOOM_LEVELS: frozenset[str] = frozenset(
    {"Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"}
)

SYSTEM_PROMPT: str = """You are an expert educator. Given course material and student notes, \
generate flashcards that test knowledge at multiple Bloom's taxonomy levels \
(Remember, Understand, Apply, Analyze, Evaluate, Create).

Rules:
- Generate between 5 and 10 flashcards.
- Blend both the course material and the student notes so that roughly half the \
cards draw from each source.
- If one source is empty, generate all cards from the other source.
- Return ONLY a valid JSON array with no extra text. Each element must be an \
object with exactly four fields:
    "question"   (string)  — the flashcard question
    "answer"     (string)  — the flashcard answer
    "difficulty" (integer) — 1 (easiest) to 5 (hardest)
    "bloom_level" (string) — one of: Remember, Understand, Apply, Analyze, Evaluate, Create

Example output format:
[
  {
    "question": "What is supervised learning?",
    "answer": "A type of ML that trains on labelled data.",
    "difficulty": 1,
    "bloom_level": "Remember"
  },
  {
    "question": "How would you apply gradient descent to minimise training loss?",
    "answer": "Compute the gradient of the loss, then update weights in the \
negative gradient direction.",
    "difficulty": 4,
    "bloom_level": "Apply"
  }
]"""


def build_user_message(module_content: str, student_notes: str) -> str:
    """Build the user-turn message that contains both learning sources.

    Args:
        module_content: Instructor-provided course material for the module.
        student_notes: The student's personal notes for the module.

    Returns:
        A formatted string combining both sources, ready to send as the
        ``"user"`` role message in the Claude API call.
    """
    return (
        f"## Course Material\n\n{module_content}\n\n"
        f"## Student Notes\n\n{student_notes}\n\n"
        "Generate flashcards that cover key concepts from both sources above."
    )
