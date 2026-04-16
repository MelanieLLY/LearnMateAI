"""SQLAlchemy ORM model for the Enrollment entity."""

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, timezone

from src.database import Base


class Enrollment(Base):
    """Represents a student enrolled in a course.

    Attributes:
        id: Auto-incremented primary key.
        student_id: Foreign key reference to the user.
        course_id: Foreign key reference to the course.
        enrolled_at: UTC timestamp.
    """

    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
