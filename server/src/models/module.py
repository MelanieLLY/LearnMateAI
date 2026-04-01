"""SQLAlchemy ORM model for the Module entity."""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, UniqueConstraint

from src.database import Base


class Module(Base):
    """Represents a learning module created and owned by an instructor.

    Attributes:
        id: Auto-incremented primary key.
        title: Human-readable module title; must be unique per instructor.
        description: Optional longer description of the module's content.
        learning_objectives: Optional learning objectives for the module.
        audience_context: Optional audience context / sensitivity context.
        instructor_id: Foreign key reference to the owning instructor's user ID.
        created_at: UTC timestamp recorded when the row is first inserted.
        updated_at: UTC timestamp refreshed on every subsequent update.
    """

    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    learning_objectives = Column(String, nullable=True)
    audience_context = Column(String, nullable=True)
    instructor_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    __table_args__ = (
        UniqueConstraint("instructor_id", "title", name="uq_instructor_title"),
    )
