from datetime import datetime

from pydantic import BaseModel, field_validator


class ModuleCreate(BaseModel):
    title: str
    description: str | None = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("title must not be empty")
        return v


class ModuleResponse(BaseModel):
    id: int
    title: str
    description: str | None
    instructor_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
