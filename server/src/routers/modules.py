"""FastAPI router for the Module resource.

All route handlers are intentionally thin: they validate input via Pydantic,
enforce auth via dependencies, and delegate business logic to ``module_service``.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.dependencies import require_instructor
from src.schemas.module import ModuleCreate, ModuleResponse, ModuleUpdate
from src.services import module_service

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


@router.put("/modules/{module_id}", response_model=ModuleResponse, status_code=200)
def edit_module(
    module_id: int,
    payload: ModuleUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_instructor),
) -> ModuleResponse:
    """Partially update a module owned by the authenticated instructor.

    Args:
        module_id: Path parameter identifying the module to update.
        payload: Validated request body; only provided fields are overwritten.
        db: Injected database session.
        current_user: Decoded JWT payload; guaranteed to have ``role == "instructor"``.

    Returns:
        The updated module serialised as a ``ModuleResponse`` with HTTP 200.

    Raises:
        HTTPException: 401 if the request is unauthenticated.
        HTTPException: 403 if the user is not an instructor or does not own the module.
        HTTPException: 404 if no module with ``module_id`` exists.
        HTTPException: 422 if the request body fails Pydantic validation.
    """
    instructor_id = int(current_user["sub"])
    return module_service.update_module(db, module_id, instructor_id, payload)


@router.delete("/modules/{module_id}", status_code=204)
def delete_module(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_instructor),
) -> None:
    """Permanently delete a module owned by the authenticated instructor.

    Args:
        module_id: Path parameter identifying the module to delete.
        db: Injected database session.
        current_user: Decoded JWT payload; guaranteed to have ``role == "instructor"``.

    Returns:
        ``None`` — FastAPI sends an empty 204 No Content response.

    Raises:
        HTTPException: 401 if the request is unauthenticated.
        HTTPException: 403 if the user is not an instructor or does not own the module.
        HTTPException: 404 if no module with ``module_id`` exists.
    """
    instructor_id = int(current_user["sub"])
    module_service.delete_module(db, module_id, instructor_id)
