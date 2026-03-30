"""SQLAlchemy ORM model for the StudentNote entity."""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text

from src.database import Base


class StudentNote(Base):
    """Represents a note uploaded by a student to a specific module.

    Attributes:
        id: Auto-incremented primary key.
        content: The full text content of the student's note.
        module_id: Foreign key reference to the module this note belongs to.
        student_id: The user ID of the student who uploaded the note.
        uploaded_at: UTC timestamp recorded when the note is first inserted.
    """

    __tablename__ = "student_notes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    student_id = Column(Integer, nullable=False)
    uploaded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
