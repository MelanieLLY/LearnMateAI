"""FastAPI router for Quiz endpoints."""

from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.dependencies import require_student
from src.schemas.quiz import QuizRequest, QuizResponse
from src.services.quiz_service import generate_and_store_quiz

router = APIRouter()


@router.post(
    "/modules/{module_id}/quizzes",
    response_model=QuizResponse,
    status_code=status.HTTP_201_CREATED,
)
def generate_quiz_endpoint(
    module_id: int,
    payload: QuizRequest = Body(default=QuizRequest()),
    user: dict = Depends(require_student),
    db: Session = Depends(get_db),
) -> QuizResponse:
    """Generate an AI-powered quiz from a module's content and store it.

    The request body is optional.  If omitted, the quiz is generated at
    ``"Medium"`` difficulty.

    Args:
        module_id: ID of the module to generate a quiz for.
        payload: Optional body containing ``difficulty_level``
            (``"Easy"``, ``"Medium"``, or ``"Hard"``).
        user: Decoded JWT payload; must have role ``"student"``.
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
    return generate_and_store_quiz(
        db=db,
        module_id=module_id,
        student_id=student_id,
        difficulty_level=payload.difficulty_level,
        num_questions=payload.num_questions,
    )
