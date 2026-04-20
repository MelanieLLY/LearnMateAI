"""Pydantic request and response schemas for the Quiz resource."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from src.agents.prompts.quiz_prompt import DIFFICULTY_LEVELS


class QuizQuestion(BaseModel):
    """Schema for a single quiz question.

    Attributes:
        id: 1-based sequential question index.
        text: The question text.
        question_type: Either ``"multiple_choice"`` or ``"short_answer"``.
        options: List of exactly 4 answer options for multiple-choice questions.
            ``None`` for short-answer questions.
        correct_answer: The correct answer string.
        explanation: A brief explanation of why the answer is correct.
    """

    id: int
    text: str
    question_type: str
    options: Optional[List[str]] = None
    correct_answer: str
    explanation: str


class QuizRequest(BaseModel):
    """Request body for the quiz generation endpoint.

    Attributes:
        difficulty_level: Desired difficulty.  Defaults to ``"Medium"``.
    """
    difficulty_level: str = "Medium"
    num_questions: int = Field(default=5, ge=1, le=15)
    @field_validator("difficulty_level")
    @classmethod
    def difficulty_level_must_be_valid(cls, v: str) -> str:
        """Ensure difficulty_level is one of the recognised levels.

        Args:
            v: The raw difficulty_level string from the request body.

        Returns:
            The validated difficulty_level string.

        Raises:
            ValueError: If *v* is not in ``DIFFICULTY_LEVELS``.
        """
        if v not in DIFFICULTY_LEVELS:
            raise ValueError(
                f"difficulty_level must be one of {sorted(DIFFICULTY_LEVELS)}, got: {v!r}"
            )
        return v
        
class QuizUpdateRequest(BaseModel):
    """Request body for updating an existing quiz.
    
    Attributes:
        title: The updated title.
        questions: The updated list of quiz questions.
    """
    title: str
    questions: List[QuizQuestion]


class QuizResponse(BaseModel):
    """Response schema for a single generated quiz.

    Attributes:
        id: Database-assigned primary key.
        module_id: ID of the module this quiz belongs to.
        student_id: ID of the student who requested the quiz.
        title: A concise title for the quiz.
        difficulty_level: The difficulty level used (Easy, Medium, or Hard).
        questions: The list of quiz questions, each as a ``QuizQuestion``.
        created_at: UTC timestamp of when the quiz was created.
    """

    id: int
    module_id: int
    student_id: int
    is_instructor_assigned: bool
    title: str
    difficulty_level: str = Field(...)
    questions: List[QuizQuestion]
    created_at: datetime

    @field_validator("difficulty_level")
    @classmethod
    def difficulty_level_must_be_valid(cls, v: str) -> str:
        """Ensure difficulty_level stored in the DB is a recognised value.

        Args:
            v: The raw difficulty_level string from the ORM object.

        Returns:
            The validated difficulty_level string.

        Raises:
            ValueError: If *v* is not in ``DIFFICULTY_LEVELS``.
        """
        if v not in DIFFICULTY_LEVELS:
            raise ValueError(
                f"difficulty_level must be one of {sorted(DIFFICULTY_LEVELS)}, got: {v!r}"
            )
        return v

    model_config = {"from_attributes": True}
