"""FastAPI router for Quiz endpoints."""

import logging

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.dependencies import require_student, require_instructor, get_current_user
from src.schemas.quiz import QuizRequest, QuizResponse, QuizUpdateRequest
from src.schemas.quiz_submission import QuizSubmissionRequest, QuizSubmissionResponse
from src.models.quiz_submission import QuizSubmission
from src.models.quiz import Quiz
from src.services.quiz_service import generate_and_store_quiz

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/modules/{module_id}/quizzes",
    response_model=QuizResponse,
    status_code=status.HTTP_201_CREATED,
)
def generate_quiz_endpoint(
    module_id: int,
    payload: QuizRequest = Body(default=QuizRequest()),
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> QuizResponse:
    """Generate an AI-powered quiz from a module's content and store it.

    The request body is optional.  If omitted, the quiz is generated at
    ``"Medium"`` difficulty.

    Args:
        module_id: ID of the module to generate a quiz for.
        payload: Optional body containing ``difficulty_level``
            (``"Easy"``, ``"Medium"``, or ``"Hard"``).
        user: Decoded JWT payload; can be any authenticated user.
        db: Active database session injected by FastAPI.

    Returns:
        The created quiz serialised as ``QuizResponse``.

    Raises:
        HTTPException: 401 if unauthenticated, 403 if not a student,
            404 if the module does not exist.

    Example request body::

        {"difficulty_level": "Hard"}

    Example response::

        {
          "id": 1,
          "module_id": 3,
          "student_id": 2,
          "title": "Neural Networks Quiz",
          "difficulty_level": "Hard",
          "questions": [
            {
              "id": 1,
              "text": "What is backpropagation?",
              "question_type": "multiple_choice",
              "options": ["A", "B", "C", "D"],
              "correct_answer": "B",
              "explanation": "..."
            }
          ],
          "created_at": "2026-04-12T10:00:00Z"
        }
    """
    student_id = int(user["sub"])
    is_instructor = user.get("role") == "instructor"
    try:
        return generate_and_store_quiz(
            db=db,
            module_id=module_id,
            student_id=student_id,
            difficulty_level=payload.difficulty_level,
            num_questions=payload.num_questions,
            is_instructor_assigned=is_instructor,
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception(
            "Quiz generation failed for module_id=%d, student_id=%d, role=%s: %s",
            module_id,
            student_id,
            user.get("role"),
            exc,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Quiz generation failed: {exc}",
        ) from exc

@router.get(
    "/modules/{module_id}/quizzes",
    response_model=list[QuizResponse],
)
def get_module_quizzes_endpoint(
    module_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve quizzes associated with a module.
    
    Instructors see quizzes assigned by instructors.
    Students see instructor assigned quizzes + their own generated quizzes.
    """
    query = db.query(Quiz).filter(Quiz.module_id == module_id)
    if user.get("role") == "student":
        student_id = int(user["sub"])
        query = query.filter(
            (Quiz.is_instructor_assigned == True) | 
            (Quiz.student_id == student_id)
        )
    else:
        query = query.filter(Quiz.is_instructor_assigned == True)
        
    return query.order_by(Quiz.created_at.desc()).all()

@router.get(
    "/quizzes/{quiz_id}",
    response_model=QuizResponse,
)
def get_quiz_endpoint(
    quiz_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Fetch an existing quiz by its ID."""
    from fastapi import HTTPException
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
        
    # Prevent students from viewing other students' quizzes
    if user.get("role") == "student" and not quiz.is_instructor_assigned and quiz.student_id != int(user["sub"]):
        raise HTTPException(status_code=403, detail="Not authorized to view this quiz")
        
    return quiz

@router.put(
    "/quizzes/{quiz_id}",
    response_model=QuizResponse,
)
def update_quiz_endpoint(
    quiz_id: int,
    payload: QuizUpdateRequest = Body(...),
    user: dict = Depends(require_instructor),
    db: Session = Depends(get_db),
):
    """Update an existing instructor-assigned quiz (e.g. edit questions)."""
    from fastapi import HTTPException
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id, Quiz.is_instructor_assigned == True).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found or not instructor assigned")
        
    quiz.title = payload.title
    quiz.questions = [q.model_dump() for q in payload.questions]
    db.commit()
    db.refresh(quiz)
    return quiz


@router.post(
    "/quizzes/{quiz_id}/submit",
    response_model=QuizSubmissionResponse,
    status_code=status.HTTP_201_CREATED,
)
def submit_quiz_endpoint(
    quiz_id: int,
    payload: QuizSubmissionRequest = Body(...),
    user: dict = Depends(require_student),
    db: Session = Depends(get_db),
) -> QuizSubmissionResponse:
    """Submit a quiz and save the score.

    Args:
        quiz_id: ID of the quiz being submitted.
        payload: Body containing the score.
        user: Decoded JWT payload; must have role ``"student"``.
        db: Active database session.

    Returns:
        The created quiz submission serialised as ``QuizSubmissionResponse``.
    """
    from fastapi import HTTPException
    student_id = int(user["sub"])
    
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
        
    submission = QuizSubmission(
        quiz_id=quiz_id,
        student_id=student_id,
        score=payload.score
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission
