"""
RED phase tests for POST /api/v1/modules (Create Module).

These tests are intentionally written BEFORE any implementation exists.
All tests must FAIL at this stage — that is the expected outcome of the RED phase.

Covered scenarios
-----------------
1. Happy Path        : valid payload + instructor token  → 201 Created
2. Missing Title     : payload without 'title' field     → 422 Unprocessable Entity
3. Empty Title       : payload with title=""             → 422 Unprocessable Entity
4. Duplicate Title   : same instructor, same title twice → 409 Conflict
5. Unauthenticated   : no Authorization header           → 401 Unauthorized
6. Wrong Role        : valid token but role='student'    → 403 Forbidden
"""

from fastapi.testclient import TestClient

BASE_URL = "/api/v1/modules"


class TestCreateModule:
    """Test suite for the Create Module API endpoint."""

    # ------------------------------------------------------------------
    # 1. Happy Path
    # ------------------------------------------------------------------

    def test_create_module_success(self, client: TestClient, instructor_token: str) -> None:
        """A valid payload submitted by an authenticated instructor returns 201.

        The response body must contain the created module's id, title,
        description, instructor_id, and created_at timestamp.
        """
        payload = {
            "title": "Intro to Python",
            "description": "A beginner-friendly Python module.",
        }

        response = client.post(
            BASE_URL,
            json=payload,
            headers={"Authorization": f"Bearer {instructor_token}"},
        )

        assert response.status_code == 201, response.text
        data = response.json()
        assert data["title"] == "Intro to Python"
        assert data["description"] == "A beginner-friendly Python module."
        assert "id" in data
        assert "instructor_id" in data
        assert "created_at" in data

    # ------------------------------------------------------------------
    # 2. Missing Title
    # ------------------------------------------------------------------

    def test_create_module_missing_title(
        self, client: TestClient, instructor_token: str
    ) -> None:
        """A payload that omits 'title' entirely returns 422 Unprocessable Entity."""
        payload = {"description": "No title provided at all."}

        response = client.post(
            BASE_URL,
            json=payload,
            headers={"Authorization": f"Bearer {instructor_token}"},
        )

        assert response.status_code == 422, response.text

    # ------------------------------------------------------------------
    # 3. Empty Title
    # ------------------------------------------------------------------

    def test_create_module_empty_title(
        self, client: TestClient, instructor_token: str
    ) -> None:
        """A payload with an empty string title returns 422 Unprocessable Entity."""
        payload = {"title": "", "description": "Title is an empty string."}

        response = client.post(
            BASE_URL,
            json=payload,
            headers={"Authorization": f"Bearer {instructor_token}"},
        )

        assert response.status_code == 422, response.text

    # ------------------------------------------------------------------
    # 4. Duplicate Title
    # ------------------------------------------------------------------

    def test_create_module_duplicate_title(
        self, client: TestClient, instructor_token: str
    ) -> None:
        """Creating two modules with the same title under the same instructor returns 409.

        The first request must succeed (201); the second must be rejected (409)
        with a detail message indicating a conflict.
        """
        payload = {"title": "Duplicate Module Title", "description": "First creation."}

        first_response = client.post(
            BASE_URL,
            json=payload,
            headers={"Authorization": f"Bearer {instructor_token}"},
        )
        assert first_response.status_code == 201, (
            f"Expected first creation to succeed, got {first_response.status_code}: "
            f"{first_response.text}"
        )

        second_response = client.post(
            BASE_URL,
            json=payload,
            headers={"Authorization": f"Bearer {instructor_token}"},
        )
        assert second_response.status_code == 409, second_response.text
        assert "already exists" in second_response.json()["detail"].lower()

    # ------------------------------------------------------------------
    # 5. Unauthenticated
    # ------------------------------------------------------------------

    def test_create_module_unauthenticated(self, client: TestClient) -> None:
        """A request with no Authorization header returns 401 Unauthorized."""
        payload = {"title": "Unauthenticated Module", "description": "No token sent."}

        response = client.post(BASE_URL, json=payload)

        assert response.status_code == 401, response.text

    # ------------------------------------------------------------------
    # 6. Wrong Role (student cannot create modules)
    # ------------------------------------------------------------------

    def test_create_module_student_role_forbidden(
        self, client: TestClient, student_token: str
    ) -> None:
        """A request authenticated as a student returns 403 Forbidden."""
        payload = {
            "title": "Student Module Attempt",
            "description": "Students cannot create modules.",
        }

        response = client.post(
            BASE_URL,
            json=payload,
            headers={"Authorization": f"Bearer {student_token}"},
        )

        assert response.status_code == 403, response.text
