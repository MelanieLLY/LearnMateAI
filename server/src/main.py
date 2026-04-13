"""LearnMateAI FastAPI application entry point.

Creates the FastAPI ``app`` instance, initialises the database schema, and
registers all API routers under the ``/api/v1`` prefix.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database import Base, engine
from src.models import flashcard  # noqa: F401 — registers ORM model
from src.models import student_note  # noqa: F401 — registers ORM model
from src.models import quiz  # noqa: F401 — registers ORM model
from src.models import summary  # noqa: F401 — registers ORM model
from src.models import user  # noqa: F401 — registers ORM model
from src.models import material  # noqa: F401
from src.routers.auth import router as auth_router
from src.routers.courses import router as courses_router
from src.routers.flashcards import router as flashcards_router
from src.routers.modules import router as modules_router
from src.routers.student_notes import router as student_notes_router
from src.routers.quizzes import router as quizzes_router
from src.routers.summaries import router as summaries_router

import os
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)

app = FastAPI(title="LearnMateAI API", version="0.1.0")

# 配置 CORS，支持前端端口波动 (例如 5200-5299 和 5100-5199)
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1):(51[0-9]{2}|52[0-9]{2})$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure CORS to allow dynamic frontend ports (e.g. 5200-5299 and 5100-5199)
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1):(51[0-9]{2}|52[0-9]{2})$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure uploads directory exists
os.makedirs("uploads/materials", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth_router, prefix="/api/v1")
app.include_router(courses_router, prefix="/api/v1")

app.include_router(modules_router, prefix="/api/v1")
app.include_router(student_notes_router, prefix="/api/v1")
app.include_router(flashcards_router, prefix="/api/v1")
app.include_router(quizzes_router, prefix="/api/v1")
app.include_router(summaries_router, prefix="/api/v1")
