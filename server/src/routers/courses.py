from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.dependencies import require_instructor
from src.schemas.course import CourseCreate, CourseResponse, CourseUpdate
from src.services import course_service

router = APIRouter()

@router.get("/courses", response_model=List[CourseResponse], status_code=200)
def get_courses(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_instructor),
):
    """Get all courses owned by the authenticated instructor."""
    instructor_id = int(current_user["sub"])
    return course_service.get_instructor_courses(db, instructor_id)

@router.post("/courses", response_model=CourseResponse, status_code=201)
def create_course(
    payload: CourseCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_instructor),
):
    """Create a new course for the authenticated instructor."""
    instructor_id = int(current_user["sub"])
    # Should probably check uniqueness of title per instructor, skipped for brevity in proto
    return course_service.create_course(db, instructor_id, payload)

@router.put("/courses/{course_id}", response_model=CourseResponse, status_code=200)
def update_course(
    course_id: int,
    payload: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_instructor),
):
    """Partially update an existing course."""
    instructor_id = int(current_user["sub"])
    return course_service.update_course(db, course_id, instructor_id, payload)

@router.delete("/courses/{course_id}", status_code=204)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_instructor),
):
    """Delete a course."""
    instructor_id = int(current_user["sub"])
    course_service.delete_course(db, course_id, instructor_id)
    return None
