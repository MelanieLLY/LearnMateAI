"""Business logic for the Flashcard resource."""

import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.agents.flashcard_agent import generate_flashcards_from_content
from src.models.flashcard import Flashcard
from src.models.module import Module

logger = logging.getLogger(__name__)


def generate_and_store_flashcards(
    db: Session,
    module_id: int,
    student_id: int,
) -> list[Flashcard]:
    """Generate flashcards from a module's content and persist them to the database.

    Args:
        db: Active SQLAlchemy database session.
        module_id: ID of the module to generate flashcards for.
        student_id: ID of the student requesting generation.

    Returns:
        A list of newly created ``Flashcard`` ORM instances.

    Raises:
        HTTPException: 404 if the module does not exist.
    """
    module = db.query(Module).filter(Module.id == module_id).first()
    if module is None:
        raise HTTPException(status_code=404, detail="Module not found")

    content = f"{module.title}\n\n{module.description or ''}"
    logger.info("Generating flashcards for module_id=%d, student_id=%d", module_id, student_id)

    raw_flashcards = generate_flashcards_from_content(content)

    flashcards = [
        Flashcard(
            question=item["question"],
            answer=item["answer"],
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
) -> list[Flashcard]:
    """Retrieve all flashcards stored for a given module.

    Args:
        db: Active SQLAlchemy database session.
        module_id: ID of the module whose flashcards to retrieve.

    Returns:
        A list of ``Flashcard`` ORM instances (may be empty).

    Raises:
        HTTPException: 404 if the module does not exist.
    """
    module = db.query(Module).filter(Module.id == module_id).first()
    if module is None:
        raise HTTPException(status_code=404, detail="Module not found")

    return db.query(Flashcard).filter(Flashcard.module_id == module_id).all()
