"""Pydantic request and response schemas for the QuizSubmission resource."""

from datetime import datetime

from pydantic import BaseModel, Field


class QuizSubmissionRequest(BaseModel):
    """Schema for submitting a quiz.

    Attributes:
        score: The calculated score percentage (0-100).
    """

    score: int = Field(..., ge=0, le=100)


class QuizSubmissionResponse(BaseModel):
    """Schema for the QuizSubmission response.

    Attributes:
        id: Database-assigned primary key.
        quiz_id: Foreign key reference to the quiz.
        student_id: The user ID of the student.
        score: The calculated score (percentage, 0-100).
        created_at: UTC timestamp.
    """

    id: int
    quiz_id: int
    student_id: int
    score: int
    created_at: datetime

    model_config = {"from_attributes": True}
