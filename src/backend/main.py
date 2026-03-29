"""LearnMateAI FastAPI application entry point.

Creates the FastAPI ``app`` instance, initialises the database schema, and
registers all API routers under the ``/api/v1`` prefix.
"""

from fastapi import FastAPI

from src.backend.database import Base, engine
from src.backend.models import flashcard  # noqa: F401 — registers ORM model
from src.backend.models import student_note  # noqa: F401 — registers ORM model
from src.backend.routers.flashcards import router as flashcards_router
from src.backend.routers.modules import router as modules_router
from src.backend.routers.student_notes import router as student_notes_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="LearnMateAI API", version="0.1.0")
app.include_router(modules_router, prefix="/api/v1")
app.include_router(student_notes_router, prefix="/api/v1")
app.include_router(flashcards_router, prefix="/api/v1")
