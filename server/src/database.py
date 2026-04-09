"""Database engine, session factory, and base model for LearnMateAI.

Defaults to an in-memory SQLite database so the test suite runs without any
external infrastructure.  Set the DATABASE_URL environment variable to a
real PostgreSQL DSN in staging and production.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool

DATABASE_URL: str = os.environ.get("DATABASE_URL", "sqlite:///./learnmate.db")

# StaticPool forces all sessions to reuse the same underlying connection.
# This is necessary for SQLite in-memory databases: without it, each new
# session would open a fresh connection and see an empty schema.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Shared declarative base for all SQLAlchemy ORM models."""


def get_db() -> Session:
    """Yield a database session and guarantee it is closed after use.

    Intended for use as a FastAPI dependency via ``Depends(get_db)``.

    Yields:
        Session: An active SQLAlchemy session bound to ``SessionLocal``.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
