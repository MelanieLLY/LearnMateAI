"""FastAPI router for Student Note endpoints."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.backend.database import get_db
from src.backend.dependencies import require_student
from src.backend.schemas.student_note import StudentNoteCreate, StudentNoteResponse
from src.backend.services.student_note_service import upload_student_note

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
