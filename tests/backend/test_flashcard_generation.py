"""
RED phase tests for Flashcard Generation endpoints.

  POST /api/v1/modules/{module_id}/flashcards  – generate & store flashcards
  GET  /api/v1/modules/{module_id}/flashcards  – retrieve stored flashcards

These tests are written BEFORE any implementation exists.
All tests must FAIL at this stage — that is the expected outcome of the RED phase.

Covered scenarios
-----------------
POST /modules/{module_id}/flashcards
  1. Happy Path       : valid student token + existing module → 201 Created, flashcards in body
  2. Unauthenticated  : no Authorization header               → 401 Unauthorized
  3. Wrong Role       : instructor token                      → 403 Forbidden
  4. Module Not Found : non-existent module_id               → 404 Not Found

GET /modules/{module_id}/flashcards
  5. Happy Path       : student token + existing module       → 200 OK, list of flashcards
  6. Module Not Found : non-existent module_id               → 404 Not Found
"""

from unittest.mock import patch

from fastapi.testclient import TestClient

BASE_URL = "/api/v1/modules"

# Canned flashcard data returned by the mocked Claude agent
MOCK_FLASHCARDS = [
    {"question": "What is machine learning?", "answer": "A subset of AI that learns from data."},
    {"question": "What is a neural network?", "answer": "A model inspired by the human brain."},
]


def _flashcards_url(module_id: int) -> str:
    """Build the flashcards endpoint URL for a given module."""
    return f"{BASE_URL}/{module_id}/flashcards"


def _auth(token: str) -> dict[str, str]:
    """Return an Authorization header dict for the given token."""
    return {"Authorization": f"Bearer {token}"}


def _create_module(client: TestClient, instructor_token: str, title: str = "Test Module") -> int:
    """Helper: create a module and return its id."""
    response = client.post(
        BASE_URL,
        json={"title": title, "description": "Module content used to generate flashcards."},
        headers=_auth(instructor_token),
    )
    assert response.status_code == 201, f"Module creation failed: {response.text}"
    return response.json()["id"]


class TestGenerateFlashcards:
    """Test suite for POST /api/v1/modules/{module_id}/flashcards."""

    def test_generate_flashcards_success(
        self, client: TestClient, student_token: str, instructor_token: str
    ) -> None:
        """A student generates flashcards for an existing module → 201 Created."""
        module_id = _create_module(client, instructor_token, title="Generate Success Module")
        with patch(
            "src.backend.agents.flashcard_agent.generate_flashcards_from_content",
            return_value=MOCK_FLASHCARDS,
        ):
            response = client.post(
                _flashcards_url(module_id),
                headers=_auth(student_token),
            )
        assert response.status_code == 201, response.text
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        first = data[0]
        assert "id" in first
        assert "question" in first
        assert "answer" in first
        assert "module_id" in first
        assert "student_id" in first
        assert "created_at" in first
        assert first["module_id"] == module_id

    def test_generate_flashcards_unauthenticated(
        self, client: TestClient, instructor_token: str
    ) -> None:
        """No Authorization header → 401 Unauthorized."""
        module_id = _create_module(client, instructor_token, title="Generate Unauth Module")
        response = client.post(_flashcards_url(module_id))
        assert response.status_code == 401, response.text

    def test_generate_flashcards_instructor_forbidden(
        self, client: TestClient, instructor_token: str
    ) -> None:
        """Instructor token → 403 Forbidden (only students may generate flashcards)."""
        module_id = _create_module(client, instructor_token, title="Generate Forbidden Module")
        with patch(
            "src.backend.agents.flashcard_agent.generate_flashcards_from_content",
            return_value=MOCK_FLASHCARDS,
        ):
            response = client.post(
                _flashcards_url(module_id),
                headers=_auth(instructor_token),
            )
        assert response.status_code == 403, response.text

    def test_generate_flashcards_module_not_found(
        self, client: TestClient, student_token: str
    ) -> None:
        """Non-existent module_id → 404 Not Found."""
        with patch(
            "src.backend.agents.flashcard_agent.generate_flashcards_from_content",
            return_value=MOCK_FLASHCARDS,
        ):
            response = client.post(
                _flashcards_url(999999),
                headers=_auth(student_token),
            )
        assert response.status_code == 404, response.text


class TestGetFlashcards:
    """Test suite for GET /api/v1/modules/{module_id}/flashcards."""

    def test_get_flashcards_success(
        self, client: TestClient, student_token: str, instructor_token: str
    ) -> None:
        """A student retrieves flashcards for a module that has some → 200 OK."""
        module_id = _create_module(client, instructor_token, title="Get Success Module")
        # First generate some flashcards
        with patch(
            "src.backend.agents.flashcard_agent.generate_flashcards_from_content",
            return_value=MOCK_FLASHCARDS,
        ):
            client.post(_flashcards_url(module_id), headers=_auth(student_token))

        response = client.get(_flashcards_url(module_id), headers=_auth(student_token))
        assert response.status_code == 200, response.text
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["module_id"] == module_id

    def test_get_flashcards_module_not_found(
        self, client: TestClient, student_token: str
    ) -> None:
        """Non-existent module_id → 404 Not Found."""
        response = client.get(_flashcards_url(999999), headers=_auth(student_token))
        assert response.status_code == 404, response.text
