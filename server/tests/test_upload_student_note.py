"""
RED phase tests for POST /api/v1/modules/{module_id}/notes (Upload Student Note).

These tests are intentionally written BEFORE any implementation exists.
All tests must FAIL at this stage — that is the expected outcome of the RED phase.

Covered scenarios
-----------------
1. Happy Path        : valid content + student token + existing module → 201 Created
2. Missing Content   : payload without 'content' field                 → 422 Unprocessable Entity
3. Empty Content     : payload with content=""                         → 422 Unprocessable Entity
4. Unauthenticated   : no Authorization header                         → 401 Unauthorized
5. Wrong Role        : valid token but role='instructor'               → 403 Forbidden
6. Module Not Found  : module_id that does not exist                   → 404 Not Found
"""

from fastapi.testclient import TestClient

BASE_URL = "/api/v1/modules"


def _notes_url(module_id: int) -> str:
    """Build the notes endpoint URL for a given module."""
    return f"{BASE_URL}/{module_id}/notes"


def _auth(token: str) -> dict[str, str]:
    """Return an Authorization header dict for the given token."""
    return {"Authorization": f"Bearer {token}"}


def _create_module(client: TestClient, instructor_token: str, title: str = "Test Module") -> int:
    """Helper: create a module and return its id."""
    response = client.post(
        BASE_URL,
        json={"title": title, "description": "A module for note upload tests."},
        headers=_auth(instructor_token),
    )
    assert response.status_code == 201, f"Module creation failed: {response.text}"
    return response.json()["id"]


class TestUploadStudentNote:
    """Test suite for the Upload Student Note API endpoint."""

    # ------------------------------------------------------------------
    # 1. Happy Path
    # ------------------------------------------------------------------

    def test_upload_note_success(
        self, client: TestClient, student_token: str, instructor_token: str
    ) -> None:
        """A valid note submitted by an authenticated student returns 201.

        The response body must contain the note's id, content, module_id,
        student_id, and uploaded_at timestamp.
        """
        module_id = _create_module(client, instructor_token)

        payload = {"content": "These are my study notes for the module."}

        response = client.post(
            _notes_url(module_id),
            json=payload,
            headers=_auth(student_token),
        )

        assert response.status_code == 201, response.text
        data = response.json()
        assert data["content"] == "These are my study notes for the module."
        assert data["module_id"] == module_id
        assert "id" in data
        assert "student_id" in data
        assert "uploaded_at" in data

    # ------------------------------------------------------------------
    # 2. Missing Content
    # ------------------------------------------------------------------

    def test_upload_note_missing_content(
        self, client: TestClient, student_token: str, instructor_token: str
    ) -> None:
        """A payload that omits 'content' entirely returns 422 Unprocessable Entity."""
        module_id = _create_module(client, instructor_token, title="Module Missing Content")

        response = client.post(
            _notes_url(module_id),
            json={},
            headers=_auth(student_token),
        )

        assert response.status_code == 422, response.text

    # ------------------------------------------------------------------
    # 3. Empty Content
    # ------------------------------------------------------------------

    def test_upload_note_empty_content(
        self, client: TestClient, student_token: str, instructor_token: str
    ) -> None:
        """A payload with an empty string content returns 422 Unprocessable Entity."""
        module_id = _create_module(client, instructor_token, title="Module Empty Content")

        response = client.post(
            _notes_url(module_id),
            json={"content": ""},
            headers=_auth(student_token),
        )

        assert response.status_code == 422, response.text

    # ------------------------------------------------------------------
    # 4. Unauthenticated
    # ------------------------------------------------------------------

    def test_upload_note_unauthenticated(
        self, client: TestClient, instructor_token: str
    ) -> None:
        """A request with no Authorization header returns 401 Unauthorized."""
        module_id = _create_module(client, instructor_token, title="Module Unauthenticated")

        response = client.post(
            _notes_url(module_id),
            json={"content": "Trying to upload without a token."},
        )

        assert response.status_code == 401, response.text

    # ------------------------------------------------------------------
    # 5. Wrong Role (instructor cannot upload notes)
    # ------------------------------------------------------------------

    def test_upload_note_instructor_role_forbidden(
        self, client: TestClient, instructor_token: str
    ) -> None:
        """A request authenticated as an instructor returns 403 Forbidden."""
        module_id = _create_module(client, instructor_token, title="Module Wrong Role")

        response = client.post(
            _notes_url(module_id),
            json={"content": "Instructors cannot upload student notes."},
            headers=_auth(instructor_token),
        )

        assert response.status_code == 403, response.text

    # ------------------------------------------------------------------
    # 6. Module Not Found
    # ------------------------------------------------------------------

    def test_upload_note_module_not_found(
        self, client: TestClient, student_token: str
    ) -> None:
        """Uploading a note to a non-existent module returns 404 Not Found."""
        response = client.post(
            _notes_url(999999),
            json={"content": "This module does not exist."},
            headers=_auth(student_token),
        )

        assert response.status_code == 404, response.text
