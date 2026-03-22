"""FastAPI router for the Module resource.

All route handlers are intentionally thin: they validate input via Pydantic,
enforce auth via dependencies, and delegate business logic to ``module_service``.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.backend.database import get_db
from src.backend.dependencies import require_instructor
from src.backend.schemas.module import ModuleCreate, ModuleResponse
from src.backend.services import module_service

router = APIRouter()


@router.post("/modules", response_model=ModuleResponse, status_code=201)
def create_module(
    payload: ModuleCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_instructor),
) -> ModuleResponse:
    """Create a new learning module owned by the authenticated instructor.

    Args:
        payload: Validated request body containing the module title and description.
        db: Injected database session.
        current_user: Decoded JWT payload; guaranteed to have ``role == "instructor"``.

    Returns:
        The created module serialised as a ``ModuleResponse`` with HTTP 201.

    Raises:
        HTTPException: 401 if the request is unauthenticated.
        HTTPException: 403 if the authenticated user is not an instructor.
        HTTPException: 409 if the instructor already owns a module with this title.
        HTTPException: 422 if the request body fails Pydantic validation.
    """
    instructor_id = int(current_user["sub"])
    return module_service.create_module(db, instructor_id, payload)
