"""Business logic for Module CRUD operations.

Routers delegate all database interaction to these functions so that route
handlers stay thin and this logic can be reused or unit-tested independently.
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.backend.models.module import Module
from src.backend.schemas.module import ModuleCreate, ModuleUpdate


def get_module_by_id(db: Session, module_id: int) -> Module | None:
    """Return the module with the given primary key, or ``None``.

    Args:
        db: The active database session.
        module_id: Primary key of the module to look up.

    Returns:
        The matching ``Module`` ORM instance, or ``None`` if not found.
    """
    return db.query(Module).filter(Module.id == module_id).first()


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


def update_module(
    db: Session, module_id: int, instructor_id: int, payload: ModuleUpdate
) -> Module:
    """Apply a partial update to an existing module and return it.

    Args:
        db: The active database session.
        module_id: Primary key of the module to update.
        instructor_id: ID of the instructor making the request.
        payload: Validated update data; only fields explicitly set by the caller
            are written — omitted fields are left unchanged.

    Returns:
        The updated and DB-refreshed ``Module`` ORM instance.

    Raises:
        HTTPException: 404 if no module with ``module_id`` exists.
        HTTPException: 403 if the module exists but belongs to a different instructor.
    """
    module = get_module_by_id(db, module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    if module.instructor_id != instructor_id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this module")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(module, field, value)

    db.commit()
    db.refresh(module)
    return module
