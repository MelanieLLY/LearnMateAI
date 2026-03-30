"""Pydantic request and response schemas for the Flashcard resource."""

from datetime import datetime

from pydantic import BaseModel


class FlashcardResponse(BaseModel):
    """Response schema for a single generated flashcard.

    Attributes:
        id: Database-assigned primary key.
        question: The flashcard question text.
        answer: The flashcard answer text.
        module_id: ID of the module this flashcard belongs to.
        student_id: ID of the student who generated the flashcard.
        created_at: UTC timestamp of when the flashcard was created.
    """

    id: int
    question: str
    answer: str
    module_id: int
    student_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
