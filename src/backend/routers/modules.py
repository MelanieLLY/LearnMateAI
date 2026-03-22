from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.backend.database import get_db
from src.backend.dependencies import require_instructor
from src.backend.models.module import Module
from src.backend.schemas.module import ModuleCreate, ModuleResponse

router = APIRouter()


@router.post("/modules", response_model=ModuleResponse, status_code=201)
def create_module(
    payload: ModuleCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_instructor),
):
    instructor_id = int(current_user["sub"])

    existing = db.query(Module).filter(
        Module.instructor_id == instructor_id,
        Module.title == payload.title,
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Module with this title already exists")

    module = Module(
        title=payload.title,
        description=payload.description,
        instructor_id=instructor_id,
    )
    db.add(module)
    db.commit()
    db.refresh(module)
    return module
