"""FastAPI router for Summary endpoints."""

from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.dependencies import require_student
from src.schemas.summary import SummaryRequest, SummaryResponse
from src.services.summary_service import generate_and_store_summary

router = APIRouter()


@router.post(
    "/modules/{module_id}/summaries",
    response_model=SummaryResponse,
    status_code=status.HTTP_201_CREATED,
)
def generate_summary_endpoint(
    module_id: int,
    payload: SummaryRequest = Body(default=SummaryRequest()),
    user: dict = Depends(require_student),
    db: Session = Depends(get_db),
) -> SummaryResponse:
    """Generate an AI-powered summary from a module's content and store it.

    The request body is optional.  If omitted, the summary is generated at the
    ``"Standard"`` comprehension level.

    Args:
        module_id: ID of the module to summarise.
        payload: Optional body containing ``summary_level``
            (``"Brief"``, ``"Standard"``, or ``"Detailed"``).
        user: Decoded JWT payload; must have role ``"student"``.
        db: Active database session injected by FastAPI.

    Returns:
        The created summary serialised as ``SummaryResponse``.

    Raises:
        HTTPException: 401 if unauthenticated, 403 if not a student,
            404 if the module does not exist.

    Example request body::

        {"summary_level": "Detailed"}

    Example response::

        {
          "id": 1,
          "title": "Introduction to Neural Networks",
          "content": "Neural networks consist of ...",
          "word_count": 210,
          "summary_level": "Detailed",
          "module_id": 3,
          "student_id": 2,
          "created_at": "2026-04-12T10:00:00Z"
        }
    """
    student_id = int(user["sub"])
    return generate_and_store_summary(
        db=db,
        module_id=module_id,
        student_id=student_id,
        summary_level=payload.summary_level,
    )
