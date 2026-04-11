"""SQLAlchemy ORM model for the Material entity."""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Material(Base):
    """Represents a learning material uploaded to a module."""

    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), nullable=False)
    filename = Column(String, nullable=False)
    url = Column(String, nullable=False)
    annotation = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
