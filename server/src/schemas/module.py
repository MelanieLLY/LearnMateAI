"""Pydantic request and response schemas for the Module resource."""

from datetime import datetime

from pydantic import BaseModel, field_validator


def _assert_title_not_empty(v: str | None) -> None:
    """Raise ``ValueError`` if ``v`` is a non-None string that is blank.

    Extracted so that both ``ModuleCreate`` and ``ModuleUpdate`` share identical
    validation logic without duplicating the condition.

    Args:
        v: The raw title value, or ``None`` when the field was omitted.

    Raises:
        ValueError: If ``v`` is not ``None`` and contains only whitespace.
    """
    if v is not None and not v.strip():
        raise ValueError("title must not be empty")


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
        """Delegate to ``_assert_title_not_empty`` and return the value unchanged.

        Args:
            v: The raw title string supplied by the caller.

        Returns:
            The original title string if validation passes.

        Raises:
            ValueError: If the title is blank or whitespace-only.
        """
        _assert_title_not_empty(v)
        return v


class ModuleUpdate(BaseModel):
    """Schema for the Edit Module request body.

    All fields are optional — only the supplied fields will be overwritten.

    Attributes:
        title: New module title.  Must be non-empty if provided.
        description: New description, or ``None`` to clear it.
    """

    title: str | None = None
    description: str | None = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str | None) -> str | None:
        """Delegate to ``_assert_title_not_empty`` and return the value unchanged.

        Args:
            v: The raw title value, or ``None`` when the field was omitted.

        Returns:
            The original value unchanged if validation passes.

        Raises:
            ValueError: If ``v`` is a non-None string that is blank after stripping.
        """
        _assert_title_not_empty(v)
        return v


class ModuleResponse(BaseModel):
    """Response schema shared by Create Module, Edit Module, and future read operations.

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
