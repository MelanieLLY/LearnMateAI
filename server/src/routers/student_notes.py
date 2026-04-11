"""FastAPI router for Student Note endpoints."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.dependencies import require_student
from src.schemas.student_note import StudentNoteCreate, StudentNoteResponse
from src.services.student_note_service import upload_student_note

router = APIRouter()


@router.post(
    "/modules/{module_id}/notes",
    response_model=StudentNoteResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_note(
    module_id: int,
    payload: StudentNoteCreate,
    user: dict = Depends(require_student),
    db: Session = Depends(get_db),
) -> StudentNoteResponse:
    """Upload a student note to a module.

    Args:
        module_id: ID of the module to attach the note to.
        payload: Validated request body with the note content.
        user: Decoded JWT payload; must have role ``"student"``.
        db: Active database session injected by FastAPI.

    Returns:
        The created note serialised as a ``StudentNoteResponse``.

    Raises:
        HTTPException: 401 if unauthenticated, 403 if not a student,
            404 if the module does not exist.
    """
    student_id = int(user["sub"])
    return upload_student_note(db=db, module_id=module_id, student_id=student_id, payload=payload)

from typing import List
from src.services.student_note_service import get_student_notes

@router.get(
    "/modules/{module_id}/notes",
    response_model=List[StudentNoteResponse],
    status_code=status.HTTP_200_OK,
)
def fetch_notes(
    module_id: int,
    user: dict = Depends(require_student),
    db: Session = Depends(get_db),
) -> List[StudentNoteResponse]:
    """Fetch all notes uploaded by the authenticated student for a module."""
    student_id = int(user["sub"])
    return get_student_notes(db=db, module_id=module_id, student_id=student_id)
