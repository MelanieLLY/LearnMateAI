"""Business logic for the Flashcard resource."""

import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.agents.flashcard_agent import generate_flashcards
from src.models.flashcard import Flashcard
from src.models.module import Module
from src.models.student_note import StudentNote

logger = logging.getLogger(__name__)


def generate_and_store_flashcards(
    db: Session,
    module_id: int,
    student_id: int,
) -> list[Flashcard]:
    """Generate flashcards from a module's content and persist them to the database.

    The function fetches the student's most recent note for the module and passes
    it alongside the module content to the FlashcardAgent.  If no note exists,
    an empty string is used and the agent generates cards from module content only.

    Args:
        db: Active SQLAlchemy database session.
        module_id: ID of the module to generate flashcards for.
        student_id: ID of the student requesting generation.

    Returns:
        A list of newly created ``Flashcard`` ORM instances, each including
        ``difficulty`` and ``bloom_level`` in addition to the base fields.

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
        "Generating flashcards for module_id=%d, student_id=%d (has_notes=%s)",
        module_id,
        student_id,
        bool(student_notes),
    )

    raw_flashcards = generate_flashcards(
        module_content=module_content,
        student_notes=student_notes,
    )

    flashcards = [
        Flashcard(
            question=item["question"],
            answer=item["answer"],
            difficulty=item["difficulty"],
            bloom_level=item["bloom_level"],
            module_id=module_id,
            student_id=student_id,
        )
        for item in raw_flashcards
    ]

    db.add_all(flashcards)
    db.commit()
    for card in flashcards:
        db.refresh(card)

    return flashcards


def get_flashcards_for_module(
    db: Session,
    module_id: int,
    student_id: int,
) -> list[Flashcard]:
    """Retrieve all flashcards stored for a given module and student.

    Args:
        db: Active SQLAlchemy database session.
        module_id: ID of the module whose flashcards to retrieve.
        student_id: ID of the student.

    Returns:
        A list of ``Flashcard`` ORM instances (may be empty).

    Raises:
        HTTPException: 404 if the module does not exist.
    """
    module = db.query(Module).filter(Module.id == module_id).first()
    if module is None:
        raise HTTPException(status_code=404, detail="Module not found")

    return db.query(Flashcard).filter(
        Flashcard.module_id == module_id,
        Flashcard.student_id == student_id
    ).all()
