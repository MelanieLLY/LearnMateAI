from datetime import datetime
from pydantic import BaseModel, Field

class CourseCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=150)
    description: str | None = Field(None, max_length=500)
    audience_context: str | None = Field(None, max_length=1000)

class CourseResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    audience_context: str | None = None
    instructor_id: int
    created_at: datetime
    updated_at: datetime
