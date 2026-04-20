from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json
import os

from src.database import get_db
from src.dependencies import require_instructor, get_current_user
from src.schemas.course import CourseCreate, CourseResponse, CourseUpdate
from src.services import course_service
from src.models.enrollment import Enrollment
from src.models.course import Course
from src.models.user import User
from src.schemas.enrollment import EnrollmentResponse

router = APIRouter()

@router.get("/courses", response_model=List[CourseResponse], status_code=200)
def get_courses(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get all courses. Instructors see their courses, students see all courses to enroll."""
    if current_user["role"] == "instructor":
        return course_service.get_instructor_courses(db, int(current_user["sub"]))
    else:
        return db.query(Course).all()

@router.get("/courses/enrolled", response_model=List[CourseResponse], status_code=200)
def get_enrolled_courses(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get courses the student is enrolled in."""
    if current_user["role"] != "student":
        raise HTTPException(status_code=403, detail="Only students can have enrollments")
    
    student_id = int(current_user["sub"])
    courses = db.query(Course).join(Enrollment).filter(Enrollment.student_id == student_id).all()
    return courses

@router.post("/courses/{course_id}/enroll", response_model=EnrollmentResponse, status_code=201)
def enroll_in_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Student enrolls in a course."""
    if current_user["role"] != "student":
        raise HTTPException(status_code=403, detail="Only students can enroll in courses")
        
    student_id = int(current_user["sub"])
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
        
    existing_enrollment = db.query(Enrollment).filter(
        Enrollment.student_id == student_id,
        Enrollment.course_id == course_id
    ).first()
    
    if existing_enrollment:
        raise HTTPException(status_code=400, detail="Already enrolled in this course")
        
    enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment

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

from src.schemas.user import UserResponse

@router.get("/courses/{course_id}/students", response_model=List[UserResponse], status_code=200)
def get_course_students(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_instructor),
):
    """Instructors can view students enrolled in this course."""
    instructor_id = int(current_user["sub"])
    course = db.query(Course).filter(Course.id == course_id, Course.instructor_id == instructor_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found or not owned by you")
        
    students = db.query(User).join(Enrollment).filter(Enrollment.course_id == course_id).all()
    return students

from src.schemas.report import CourseReportResponse, ModuleStat

@router.get("/courses/{course_id}/report", response_model=CourseReportResponse, status_code=200)
def get_course_report(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_instructor),
):
    """Get aggregated class report for a course."""
    instructor_id = int(current_user["sub"])
    course = db.query(Course).filter(Course.id == course_id, Course.instructor_id == instructor_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found or not owned by you")
        
    students = db.query(User).join(Enrollment).filter(Enrollment.course_id == course_id).all()
    total_students = len(students)
    
    # Read mock dat to get report stats based on course title
    root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    json_path = os.path.join(root_path, "mock_data.json")
    
    mock_report = None
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            mock_data = json.load(f)
            for c in mock_data.get("courses", []):
                if c.get("title") == course.title:
                    mock_report = c.get("report")
                    break
                    
    if not mock_report:
        mock_report = {
            "overall_average": 0,
            "common_gaps": [],
            "module_stats": []
        }
        
    # Query real overall average from QuizSubmissions
    from sqlalchemy.sql import func
    from src.models.quiz_submission import QuizSubmission
    from src.models.quiz import Quiz
    from src.models.module import Module
    
    avg_score = db.query(func.avg(QuizSubmission.score)).join(Quiz).join(Module).filter(
        Module.course_id == course_id
    ).scalar()
    
    real_average = int(avg_score) if avg_score is not None else mock_report.get("overall_average", 0)
    
    return CourseReportResponse(
        overall_average=real_average,
        total_students=total_students,
        common_gaps=mock_report.get("common_gaps", []),
        module_stats=[ModuleStat(**m) for m in mock_report.get("module_stats", [])]
    )

