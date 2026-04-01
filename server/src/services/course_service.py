from sqlalchemy.orm import Session
from src.models.course import Course
from src.schemas.course import CourseCreate

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
