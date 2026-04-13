"""Pydantic request and response schemas for the Flashcard resource."""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from src.agents.prompts.flashcard_prompt import BLOOM_LEVELS


class FlashcardResponse(BaseModel):
    """Response schema for a single generated flashcard.

    Attributes:
        id: Database-assigned primary key.
        question: The flashcard question text.
        answer: The flashcard answer text.
        difficulty: AI-assigned difficulty rating (1 = easiest, 5 = hardest).
        bloom_level: Bloom's taxonomy level for the question.
        module_id: ID of the module this flashcard belongs to.
        student_id: ID of the student who generated the flashcard.
        created_at: UTC timestamp of when the flashcard was created.
    """

    id: int
    question: str
    answer: str
    difficulty: int = Field(..., ge=1, le=5)
    bloom_level: str
    module_id: int
    student_id: int
    created_at: datetime

    @field_validator("bloom_level")
    @classmethod
    def bloom_level_must_be_valid(cls, v: str) -> str:
        """Ensure bloom_level is one of the recognised Bloom's taxonomy levels.

        Args:
            v: The raw bloom_level string from the ORM object.

        Returns:
            The validated bloom_level string.

        Raises:
            ValueError: If *v* is not in ``BLOOM_LEVELS``.
        """
        if v not in BLOOM_LEVELS:
            raise ValueError(
                f"bloom_level must be one of {sorted(BLOOM_LEVELS)}, got: {v!r}"
            )
        return v

    model_config = {"from_attributes": True}
