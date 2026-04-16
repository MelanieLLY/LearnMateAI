from pydantic import BaseModel
from datetime import datetime

class EnrollmentBase(BaseModel):
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentResponse(EnrollmentBase):
    id: int
    student_id: int
    enrolled_at: datetime

    class Config:
        from_attributes = True
