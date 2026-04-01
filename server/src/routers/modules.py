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


from fastapi import UploadFile, File, HTTPException
import boto3
import os
import uuid

import shutil

def _upload_material(file: UploadFile) -> str:
    """Storage Abstraction: Saves to S3 if AWS config is present, otherwise falls back to local storage."""
    file_extension = file.filename.split(".")[-1] if "." in file.filename else ""
    unique_name = f"{uuid.uuid4()}.{file_extension}"
    
    if os.environ.get("AWS_ACCESS_KEY_ID"):
        bucket_name = os.environ.get("S3_BUCKET_NAME", "mock-bucket")
        s3_key = f"materials/{unique_name}"
        s3 = boto3.client("s3")
        s3.upload_fileobj(file.file, bucket_name, s3_key)
        return f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"
    
    # Fallback: Save to local disk for development & affordability
    local_path = os.path.join("uploads", "materials", unique_name)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    with open(local_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return f"/uploads/materials/{unique_name}"

@router.post("/modules/{module_id}/materials", status_code=201)
def upload_material(
    module_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_instructor),
):
    """Upload a material to S3 for the specified module."""
    instructor_id = int(current_user["sub"])
    
    # Check if module exists and belongs to instructor
    module = module_service.get_module_by_id(db, module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    if module.instructor_id != instructor_id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this module")
        
    if not file:
        raise HTTPException(status_code=422, detail="No file provided")
        
    url = _upload_material(file)
    
    return {
        "id": module.id,
        "filename": file.filename,
        "url": url
    }
