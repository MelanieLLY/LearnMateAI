"""SQLAlchemy ORM model for the QuizSubmission entity."""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer

from src.database import Base


class QuizSubmission(Base):
    """Represents a student's submission for a quiz.

    Attributes:
        id: Auto-incremented primary key.
        quiz_id: Foreign key reference to the quiz.
        student_id: The user ID of the student.
        score: The calculated score (percentage, 0-100).
        created_at: UTC timestamp recorded when the submission is made.
    """

    __tablename__ = "quiz_submissions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    score = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
