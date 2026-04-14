"""Prompt templates and constants for the SummaryAgent.

This module is the single source of truth for the system prompt, allowed
summary levels, and the user-message builder used by
``summary_agent.generate_summary``.  Keeping prompts here makes it easy
to iterate on the prompt independently from the agent logic.
"""

SUMMARY_LEVELS: frozenset[str] = frozenset({"Brief", "Standard", "Detailed"})

SYSTEM_PROMPT: str = """You are an expert educator. Given course material and student notes, \
generate a synthesised summary at the requested comprehension level.

Word-count targets by level:
  Brief    — 50 to 100 words
  Standard — 150 to 250 words
  Detailed — 300 to 500 words

Rules:
- Blend both sources so the summary reflects concepts from the course material \
AND the student notes.
- If one source is empty, summarise the other source only.
- Use the provided structured output tool schema. The object must have \
exactly four fields:
    "title"         (string)  — a concise title for the summary
    "content"       (string)  — the summary text at the requested level
    "word_count"    (integer) — the number of words in "content"
    "summary_level" (string)  — one of: Brief, Standard, Detailed

Example output (Standard level):
{
  "title": "Introduction to Neural Networks",
  "content": "Neural networks consist of interconnected layers that transform \
inputs using learned weights and activation functions such as ReLU or sigmoid. \
Deep learning uses many hidden layers to capture hierarchical features. \
Backpropagation computes gradients layer by layer via the chain rule, \
enabling the network to minimise a loss function on labelled data.",
  "word_count": 53,
  "summary_level": "Standard"
}"""


def build_summary_user_message(
    module_content: str,
    student_notes: str,
    summary_level: str,
) -> str:
    """Build the user-turn message that contains both learning sources and the requested level.

    Args:
        module_content: Instructor-provided course material for the module.
        student_notes: The student's personal notes for the module.
        summary_level: One of ``SUMMARY_LEVELS`` indicating the desired depth.

    Returns:
        A formatted string combining both sources and the level instruction,
        ready to send as the ``"user"`` role message in the Claude API call.
    """
    return (
        f"## Course Material\n\n{module_content}\n\n"
        f"## Student Notes\n\n{student_notes}\n\n"
        f"Generate a {summary_level} summary of the key concepts above."
    )
