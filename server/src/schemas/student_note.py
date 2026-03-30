"""Pydantic request and response schemas for the StudentNote resource."""

from datetime import datetime

from pydantic import BaseModel, field_validator


class StudentNoteCreate(BaseModel):
    """Schema for the Upload Student Note request body.

    Attributes:
        content: Required note content. Must be a non-empty, non-whitespace string.
    """

    content: str

    @field_validator("content")
    @classmethod
    def content_must_not_be_empty(cls, v: str) -> str:
        """Reject blank or whitespace-only content.

        Args:
            v: The raw content string supplied by the caller.

        Returns:
            The original content string if validation passes.

        Raises:
            ValueError: If the content is blank or whitespace-only.
        """
        if not v.strip():
            raise ValueError("content must not be empty")
        return v


class StudentNoteResponse(BaseModel):
    """Response schema for a successfully uploaded student note.

    Attributes:
        id: Database-assigned primary key.
        content: The note content as stored.
        module_id: ID of the module this note belongs to.
        student_id: ID of the student who uploaded the note.
        uploaded_at: UTC timestamp of when the note was uploaded.
    """

    id: int
    content: str
    module_id: int
    student_id: int
    uploaded_at: datetime

    model_config = {"from_attributes": True}
