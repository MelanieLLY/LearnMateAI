"""Pydantic request and response schemas for the Summary resource."""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from src.agents.prompts.summary_prompt import SUMMARY_LEVELS


class SummaryRequest(BaseModel):
    """Request body for the summary generation endpoint.

    Attributes:
        summary_level: Desired comprehension depth.  Defaults to ``"Standard"``.
    """

    summary_level: str = "Standard"

    @field_validator("summary_level")
    @classmethod
    def summary_level_must_be_valid(cls, v: str) -> str:
        """Ensure summary_level is one of the recognised depth levels.

        Args:
            v: The raw summary_level string from the request body.

        Returns:
            The validated summary_level string.

        Raises:
            ValueError: If *v* is not in ``SUMMARY_LEVELS``.
        """
        if v not in SUMMARY_LEVELS:
            raise ValueError(
                f"summary_level must be one of {sorted(SUMMARY_LEVELS)}, got: {v!r}"
            )
        return v


class SummaryResponse(BaseModel):
    """Response schema for a single generated summary.

    Attributes:
        id: Database-assigned primary key.
        title: A concise title for the summary.
        content: The full summary text.
        word_count: Number of words in ``content``.
        summary_level: The comprehension depth used (Brief, Standard, or Detailed).
        module_id: ID of the module this summary belongs to.
        student_id: ID of the student who requested the summary.
        created_at: UTC timestamp of when the summary was created.
    """

    id: int
    title: str
    content: str
    word_count: int = Field(..., ge=1)
    summary_level: str
    module_id: int
    student_id: int
    created_at: datetime

    @field_validator("summary_level")
    @classmethod
    def summary_level_must_be_valid(cls, v: str) -> str:
        """Ensure summary_level stored in the DB is a recognised value.

        Args:
            v: The raw summary_level string from the ORM object.

        Returns:
            The validated summary_level string.

        Raises:
            ValueError: If *v* is not in ``SUMMARY_LEVELS``.
        """
        if v not in SUMMARY_LEVELS:
            raise ValueError(
                f"summary_level must be one of {sorted(SUMMARY_LEVELS)}, got: {v!r}"
            )
        return v

    model_config = {"from_attributes": True}
