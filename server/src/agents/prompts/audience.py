"""Instructor audience guidelines for the generation agents' system prompts.

Instructors describe who is in their class in ``audience_context`` on the
course and, optionally, on a module: for example a class with students who
have lost a parent, or a girls' school that wants women as positive examples.
The quiz, flashcard and summary agents append that text to their system
prompt so every generated example follows it. The guidelines shape content
and tone only; the output-format rules in each agent's base prompt still
apply. Design origin: the "Audience Context / Sensitivity" field planned in
fc085be (#15), which stored the field but did not send it to the agents.
"""

# Same limit as the course schema (src/schemas/course.py); the module field has
# no length limit, so the prompt builder enforces it for both levels.
MAX_AUDIENCE_CHARS: int = 1000
# Both levels at full length plus their "Class: " / "Module: " labels.
MAX_GUIDELINES_CHARS: int = 2 * MAX_AUDIENCE_CHARS + len("Class: \nModule: ")

_GUIDELINES_HEADER: str = """

## Audience guidelines from the instructor

The instructor of this class wrote the guidelines below about their students. \
Follow them in every example, scenario, name and wording you generate. If an \
example from the course material conflicts with them, replace it with one \
that does not. They shape content and tone only and never change the output \
format rules above.

"""


def combine_audience_context(course_context: str | None, module_context: str | None) -> str:
    """Merge course-level and module-level guidelines into one labelled text.

    Args:
        course_context: ``Course.audience_context``; applies to every module in
            the class.
        module_context: ``Module.audience_context``; extra guidance for one module.

    Returns:
        The non-empty levels, course first, each on its own labelled line, or an
        empty string when neither level has text.
    """
    parts = []
    if course_context and course_context.strip():
        parts.append(f"Class: {course_context.strip()[:MAX_AUDIENCE_CHARS]}")
    if module_context and module_context.strip():
        parts.append(f"Module: {module_context.strip()[:MAX_AUDIENCE_CHARS]}")
    return "\n".join(parts)


def with_audience_guidelines(base_prompt: str, audience_context: str) -> str:
    """Append the instructor's audience guidelines to an agent's system prompt.

    Args:
        base_prompt: The agent's ``SYSTEM_PROMPT``.
        audience_context: Guidelines text, usually from
            :func:`combine_audience_context`. Blank text adds nothing.

    Returns:
        ``base_prompt`` unchanged when there are no guidelines, otherwise
        ``base_prompt`` followed by the guidelines section.
    """
    guidelines = audience_context.strip()
    if not guidelines:
        return base_prompt
    return base_prompt + _GUIDELINES_HEADER + guidelines[:MAX_GUIDELINES_CHARS]
