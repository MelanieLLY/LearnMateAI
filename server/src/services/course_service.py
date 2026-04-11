from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.models.course import Course
from src.schemas.course import CourseCreate, CourseUpdate

def create_course(db: Session, instructor_id: int, payload: CourseCreate) -> Course:
    db_course = Course(**payload.model_dump(), instructor_id=instructor_id)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def get_instructor_courses(db: Session, instructor_id: int) -> list[Course]:
    return db.query(Course).filter(Course.instructor_id == instructor_id).all()

def get_course_by_id(db: Session, course_id: int) -> Course | None:
    return db.query(Course).filter(Course.id == course_id).first()

def update_course(db: Session, course_id: int, instructor_id: int, payload: CourseUpdate) -> Course:
    course = get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if course.instructor_id != instructor_id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this course")
        
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(course, key, value)
        
    db.commit()
    db.refresh(course)
    return course

def delete_course(db: Session, course_id: int, instructor_id: int):
    course = get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if course.instructor_id != instructor_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this course")
        
    db.delete(course)
    db.commit()
