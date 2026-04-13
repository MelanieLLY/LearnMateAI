"""Business logic for the Summary resource."""

import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.agents.summary_agent import generate_summary
from src.models.module import Module
from src.models.student_note import StudentNote
from src.models.summary import Summary

logger = logging.getLogger(__name__)


def generate_and_store_summary(
    db: Session,
    module_id: int,
    student_id: int,
    summary_level: str = "Standard",
) -> Summary:
    """Generate a summary from a module's content and persist it to the database.

    The function fetches the student's most recent note for the module and passes
    it alongside the module content to the SummaryAgent.  If no note exists, an
    empty string is used and the agent summarises from module content only.

    ``word_count`` is recomputed from the stored ``content`` at write time
    (``len(content.split())``) rather than trusting the value returned by Claude,
    ensuring the stored value is always the ground truth.

    Args:
        db: Active SQLAlchemy database session.
        module_id: ID of the module to summarise.
        student_id: ID of the student requesting generation.
        summary_level: Desired comprehension depth — one of ``"Brief"``,
            ``"Standard"``, or ``"Detailed"``.  Defaults to ``"Standard"``.

    Returns:
        A newly created ``Summary`` ORM instance with all fields populated.

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
        "Generating summary for module_id=%d, student_id=%d, level=%s (has_notes=%s)",
        module_id,
        student_id,
        summary_level,
        bool(student_notes),
    )

    raw = generate_summary(
        module_content=module_content,
        student_notes=student_notes,
        summary_level=summary_level,
    )

    # Recompute word_count from the actual stored content for accuracy.
    word_count = len(raw["content"].split())

    summary = Summary(
        title=raw["title"],
        content=raw["content"],
        word_count=word_count,
        summary_level=raw["summary_level"],
        module_id=module_id,
        student_id=student_id,
    )

    db.add(summary)
    db.commit()
    db.refresh(summary)

    return summary
