"""
Pytest fixtures shared across all backend tests.

Provides a TestClient, an in-memory SQLite database session,
and pre-built JWT tokens for different user roles.
"""

import os

import pytest
from fastapi.testclient import TestClient
from jose import jwt

# Use a fixed secret so tokens generated here match what the app will verify.
# The app reads this from the TEST_SECRET_KEY env var (set below before import).
TEST_SECRET_KEY = "test-only-secret-key-do-not-use-in-production"
ALGORITHM = "HS256"

os.environ["SECRET_KEY"] = TEST_SECRET_KEY


from src.backend.main import app  # noqa: E402  (must come after env var is set)


def _make_token(user_id: int, role: str) -> str:
    """Encode a JWT with the given user_id and role."""
    return jwt.encode({"sub": str(user_id), "role": role}, TEST_SECRET_KEY, algorithm=ALGORITHM)


@pytest.fixture
def client() -> TestClient:
    """Return a synchronous HTTPX test client bound to the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def instructor_token() -> str:
    """JWT for a user with the 'instructor' role (user_id=1)."""
    return _make_token(user_id=1, role="instructor")


@pytest.fixture
def student_token() -> str:
    """JWT for a user with the 'student' role (user_id=2)."""
    return _make_token(user_id=2, role="student")
