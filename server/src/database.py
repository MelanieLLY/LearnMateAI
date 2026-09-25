"""Database engine, session factory, and base model for LearnMateAI.

Defaults to an in-memory SQLite database so the test suite runs without any
external infrastructure.  Set the DATABASE_URL environment variable to a
real PostgreSQL DSN in staging and production.
"""

import os
import logging
import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("learnmate.database")

INIT_DB_MAX_ATTEMPTS = 5
INIT_DB_BASE_DELAY_SECONDS = 2

env_db_url = os.environ.get("DATABASE_URL")

if env_db_url and env_db_url.startswith("postgres"):
    DATABASE_URL = env_db_url
    # Render's external URL enforces SSL server-side; "prefer" also works with the
    # internal URL. Render drops idle connections, so enable TCP keepalives and
    # recycle pooled connections well before they go stale.
    engine_kwargs = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "connect_args": {
            "sslmode": "prefer",
            "connect_timeout": 10,
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 5,
        },
    }
    logger.info("Using Cloud PostgreSQL database.")
elif env_db_url and env_db_url.startswith("sqlite"):
    # e.g. "sqlite://" (in-memory) used by the test suite
    DATABASE_URL = env_db_url
    engine_kwargs = {
        "connect_args": {"check_same_thread": False},
        "poolclass": StaticPool,
    }
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


def init_db(max_attempts: int = INIT_DB_MAX_ATTEMPTS) -> None:
    """Create all tables, retrying on transient connection failures.

    Render's Postgres may briefly reject connections while the service boots
    (e.g. "SSL connection has been closed unexpectedly"), so retry with
    exponential backoff instead of crashing the process on the first failure.

    Args:
        max_attempts: Maximum number of connection attempts before re-raising.

    Raises:
        OperationalError: If the database is still unreachable after all attempts.
    """
    for attempt in range(1, max_attempts + 1):
        try:
            Base.metadata.create_all(bind=engine)
            return
        except OperationalError as exc:
            if attempt == max_attempts:
                logger.error("Database unreachable after %d attempts.", max_attempts)
                raise
            delay = INIT_DB_BASE_DELAY_SECONDS * 2 ** (attempt - 1)
            logger.warning(
                "Database connection failed (attempt %d/%d): %s. Retrying in %ds...",
                attempt, max_attempts, exc.orig, delay,
            )
            time.sleep(delay)


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
