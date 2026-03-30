"""FastAPI router for Flashcard endpoints."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.dependencies import require_student
from src.schemas.flashcard import FlashcardResponse
from src.services.flashcard_service import (
    generate_and_store_flashcards,
    get_flashcards_for_module,
)

router = APIRouter()


@router.post(
    "/modules/{module_id}/flashcards",
    response_model=list[FlashcardResponse],
    status_code=status.HTTP_201_CREATED,
)
def generate_flashcards(
    module_id: int,
    user: dict = Depends(require_student),
    db: Session = Depends(get_db),
) -> list[FlashcardResponse]:
    """Generate AI-powered flashcards from a module's content and store them.

    Args:
        module_id: ID of the module to generate flashcards for.
        user: Decoded JWT payload; must have role ``"student"``.
        db: Active database session injected by FastAPI.

    Returns:
        A list of created flashcards serialised as ``FlashcardResponse``.

    Raises:
        HTTPException: 401 if unauthenticated, 403 if not a student,
            404 if the module does not exist.
    """
    student_id = int(user["sub"])
    return generate_and_store_flashcards(db=db, module_id=module_id, student_id=student_id)


@router.get(
    "/modules/{module_id}/flashcards",
    response_model=list[FlashcardResponse],
    status_code=status.HTTP_200_OK,
)
def get_flashcards(
    module_id: int,
    user: dict = Depends(require_student),
    db: Session = Depends(get_db),
) -> list[FlashcardResponse]:
    """Retrieve all flashcards stored for a given module.

    Args:
        module_id: ID of the module whose flashcards to retrieve.
        user: Decoded JWT payload; must have role ``"student"``.
        db: Active database session injected by FastAPI.

    Returns:
        A list of flashcards serialised as ``FlashcardResponse``.

    Raises:
        HTTPException: 401 if unauthenticated, 403 if not a student,
            404 if the module does not exist.
    """
    return get_flashcards_for_module(db=db, module_id=module_id)
