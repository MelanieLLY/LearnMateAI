"""Business logic for the Quiz resource."""

import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.agents.quiz_agent import generate_quiz
from src.models.module import Module
from src.models.quiz import Quiz
from src.models.student_note import StudentNote

logger = logging.getLogger(__name__)


def generate_and_store_quiz(
    db: Session,
    module_id: int,
    student_id: int,
    difficulty_level: str = "Medium",
    num_questions: int = 5,
) -> Quiz:
    """Generate a quiz from a module's content and persist it to the database.

    The function fetches the student's most recent note for the module and
    passes it alongside the module content to the QuizAgent.  If no note
    exists, an empty string is used and the agent generates questions from
    module content only.

    The ``questions`` list is stored as-is in the JSON column — no post-
    processing is applied.

    Args:
        db: Active SQLAlchemy database session.
        module_id: ID of the module to generate a quiz for.
        student_id: ID of the student requesting generation.
        difficulty_level: Desired difficulty — one of ``"Easy"``, ``"Medium"``,
            or ``"Hard"``.  Defaults to ``"Medium"``.
        num_questions: Exact number of questions to generate. Defaults to 5.

    Returns:
        A newly created ``Quiz`` ORM instance with all fields populated,
        including the serialised ``questions`` JSON column.

    Raises:
        HTTPException: 404 if the module does not exist.
    """
    module = db.query(Module).filter(Module.id == module_id).first()
    if module is None:
        raise HTTPException(status_code=404, detail="Module not found")

    module_content = f"{module.title}\n\n{module.description or ''}"

    latest_note = (
        db.query(StudentNote)
        .filter(
            StudentNote.module_id == module_id,
            StudentNote.student_id == student_id,
        )
        .order_by(StudentNote.uploaded_at.desc())
        .first()
    )
    student_notes = latest_note.content if latest_note else ""

    logger.info(
        "Generating quiz for module_id=%d, student_id=%d, difficulty=%s (has_notes=%s)",
        module_id,
        student_id,
        difficulty_level,
        bool(student_notes),
    )

    raw = generate_quiz(
        module_content=module_content,
        student_notes=student_notes,
        difficulty_level=difficulty_level,
        num_questions=num_questions,
    )

    quiz = Quiz(
        title=raw["title"],
        difficulty_level=raw["difficulty_level"],
        questions=raw["questions"],
        module_id=module_id,
        student_id=student_id,
    )

    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    return quiz
