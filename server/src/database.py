"""Database engine, session factory, and base model for LearnMateAI.

Defaults to an in-memory SQLite database so the test suite runs without any
external infrastructure.  Set the DATABASE_URL environment variable to a
real PostgreSQL DSN in staging and production.
"""

import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("learnmate.database")

env_db_url = os.environ.get("DATABASE_URL")

if env_db_url and env_db_url.startswith("postgres"):
    # Strip SQLite-specific args from the URL just in case
    DATABASE_URL = env_db_url.replace("?check_same_thread=False", "")
    engine_kwargs = {}
    logger.info("✅ Connected to Cloud PostgreSQL Database!")
else:
    DATABASE_URL = "sqlite:///./learnmate.db"
    engine_kwargs = {
        "connect_args": {"check_same_thread": False},
        "poolclass": StaticPool,
    }
    logger.warning("⚠️ DATABASE_URL not found or invalid. Falling back to local SQLite: learnmate.db")

engine = create_engine(DATABASE_URL, **engine_kwargs)

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
