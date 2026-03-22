"""Business logic for Module CRUD operations.

Routers delegate all database interaction to these functions so that route
handlers stay thin and this logic can be reused or unit-tested independently.
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.backend.models.module import Module
from src.backend.schemas.module import ModuleCreate


def get_module_by_title(db: Session, instructor_id: int, title: str) -> Module | None:
    """Return the module matching the given instructor and title, or ``None``.

    Args:
        db: The active database session.
        instructor_id: ID of the instructor who owns the module.
        title: Exact title to look up.

    Returns:
        The matching ``Module`` ORM instance, or ``None`` if not found.
    """
    return (
        db.query(Module)
        .filter(Module.instructor_id == instructor_id, Module.title == title)
        .first()
    )


def create_module(db: Session, instructor_id: int, payload: ModuleCreate) -> Module:
    """Persist a new module for the given instructor and return it.

    Args:
        db: The active database session.
        instructor_id: ID of the instructor creating the module.
        payload: Validated request data containing ``title`` and optional ``description``.

    Returns:
        The newly created and DB-refreshed ``Module`` ORM instance.

    Raises:
        HTTPException: 409 Conflict if the instructor already owns a module with
            the same title.
    """
    if get_module_by_title(db, instructor_id, payload.title):
        raise HTTPException(
            status_code=409,
            detail="Module with this title already exists",
        )

    module = Module(
        title=payload.title,
        description=payload.description,
        instructor_id=instructor_id,
    )
    db.add(module)
    db.commit()
    db.refresh(module)
    return module
