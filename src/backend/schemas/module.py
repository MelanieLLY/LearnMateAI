"""Pydantic request and response schemas for the Module resource."""

from datetime import datetime

from pydantic import BaseModel, field_validator


class ModuleCreate(BaseModel):
    """Schema for the Create Module request body.

    Attributes:
        title: Required module title.  Must be a non-empty, non-whitespace string.
        description: Optional plain-text description of the module's content.
    """

    title: str
    description: str | None = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        """Reject titles that are empty or contain only whitespace.

        Args:
            v: The raw title value supplied by the caller.

        Returns:
            The original title string, unchanged, if it passes validation.

        Raises:
            ValueError: If ``v`` is blank after stripping leading/trailing whitespace.
        """
        if not v.strip():
            raise ValueError("title must not be empty")
        return v


class ModuleResponse(BaseModel):
    """Schema for the Create Module (and future List/Get) response body.

    Attributes:
        id: Database-assigned primary key.
        title: Module title as stored.
        description: Module description, or ``None`` if not provided.
        instructor_id: ID of the instructor who owns this module.
        created_at: UTC timestamp of when the module was created.
    """

    id: int
    title: str
    description: str | None
    instructor_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
