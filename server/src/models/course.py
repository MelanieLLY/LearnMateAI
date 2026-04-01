"""SQLAlchemy ORM model for the Course (Class) entity."""
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String, UniqueConstraint
from src.database import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    audience_context = Column(String, nullable=True)
    instructor_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    __table_args__ = (
        UniqueConstraint("instructor_id", "title", name="uq_course_instructor_title"),
    )
