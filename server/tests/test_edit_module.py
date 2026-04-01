"""
RED phase tests for PUT /api/v1/modules/{module_id} (Edit Module).

These tests are intentionally written BEFORE any implementation exists.
All tests must FAIL at this stage — that is the expected outcome of the RED phase.

Helper
------
``_auth(token)`` — builds the Authorization header dict to keep test bodies concise.

Covered scenarios
-----------------
1. Happy Path        : valid payload + owning instructor token  → 200, updated fields returned
2. Not Found         : module_id that does not exist            → 404 with "not found" detail
3. Unauthenticated   : no Authorization header                  → 401 Unauthorized
4. Wrong Role        : valid token but role='student'           → 403 Forbidden
5. Wrong Owner       : different instructor tries to edit       → 403 Forbidden
"""

import pytest
from fastapi.testclient import TestClient

BASE_URL = "/api/v1/modules"


def _auth(token: str) -> dict:
    """Return an Authorization header dict for the given Bearer token."""
    return {"Authorization": f"Bearer {token}"}


def _create_module(client: TestClient, token: str, title: str, description: str = "desc") -> int:
    """Helper: create a module and return its id.  Asserts 201 so failures are obvious."""
    resp = client.post(BASE_URL, json={"title": title, "description": description}, headers=_auth(token))
    assert resp.status_code == 201, f"Setup failed creating module: {resp.text}"
    return resp.json()["id"]


class TestEditModule:
    """Test suite for the Edit Module API endpoint (PUT /api/v1/modules/{module_id})."""

    # ------------------------------------------------------------------
    # 1. Happy Path
    # ------------------------------------------------------------------

    def test_edit_module_success(self, client: TestClient, instructor_token: str) -> None:
        """Owner sends valid update payload → 200 with the updated module data.

        Both title and description must reflect the new values in the response.
        The module id and instructor_id must remain unchanged.
        """
        module_id = _create_module(client, instructor_token, "Original Title", "Original desc")

        response = client.put(
            f"{BASE_URL}/{module_id}",
            json={
                "title": "Updated Title",
                "description": "Updated desc",
                "learning_objectives": "Updated objectives",
                "audience_context": "Updated context"
            },
            headers=_auth(instructor_token),
        )

        assert response.status_code == 200, response.text
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == "Updated desc"
        assert data["learning_objectives"] == "Updated objectives"
        assert data["audience_context"] == "Updated context"
        assert data["id"] == module_id
        assert "instructor_id" in data

    def test_edit_module_partial_update(self, client: TestClient, instructor_token: str) -> None:
        """Sending only 'description' leaves title unchanged → 200.

        Edit accepts partial payloads: omitted fields must not be overwritten.
        """
        module_id = _create_module(client, instructor_token, "Partial Update Title")

        response = client.put(
            f"{BASE_URL}/{module_id}",
            json={"learning_objectives": "Only objectives changed"},
            headers=_auth(instructor_token),
        )

        assert response.status_code == 200, response.text
        data = response.json()
        assert data["title"] == "Partial Update Title"
        assert data["learning_objectives"] == "Only objectives changed"

    # ------------------------------------------------------------------
    # 2. Not Found
    # ------------------------------------------------------------------

    def test_edit_module_not_found(self, client: TestClient, instructor_token: str) -> None:
        """Editing a non-existent module_id returns 404 with a meaningful detail message.

        The detail must confirm the module was not found (not a generic FastAPI 404),
        proving the route exists and performed a real DB lookup.
        """
        response = client.put(
            f"{BASE_URL}/99999",
            json={"title": "Ghost module"},
            headers=_auth(instructor_token),
        )

        assert response.status_code == 404, response.text
        # "module" must appear in the detail to prove a real DB lookup happened,
        # not just FastAPI's generic route-missing 404 {"detail": "Not Found"}.
        assert "module" in response.json()["detail"].lower()

    # ------------------------------------------------------------------
    # 3. Unauthenticated
    # ------------------------------------------------------------------

    def test_edit_module_unauthenticated(self, client: TestClient) -> None:
        """A request with no Authorization header returns 401 Unauthorized."""
        response = client.put(f"{BASE_URL}/1", json={"title": "No token"})

        assert response.status_code == 401, response.text

    # ------------------------------------------------------------------
    # 4. Wrong Role (student cannot edit modules)
    # ------------------------------------------------------------------

    def test_edit_module_student_role_forbidden(
        self, client: TestClient, student_token: str
    ) -> None:
        """A request authenticated as a student returns 403 Forbidden."""
        response = client.put(
            f"{BASE_URL}/1",
            json={"title": "Student edit attempt"},
            headers=_auth(student_token),
        )

        assert response.status_code == 403, response.text

    # ------------------------------------------------------------------
    # 5. Wrong Owner (different instructor cannot edit another's module)
    # ------------------------------------------------------------------

    def test_edit_module_wrong_instructor(
        self,
        client: TestClient,
        instructor_token: str,
        second_instructor_token: str,
    ) -> None:
        """Instructor 2 cannot edit a module owned by Instructor 1 → 403 Forbidden.

        This enforces that ownership is checked, not just the role.
        """
        module_id = _create_module(client, instructor_token, "Instructor 1 Owns This")

        response = client.put(
            f"{BASE_URL}/{module_id}",
            json={"title": "Hijacked by Instructor 2"},
            headers=_auth(second_instructor_token),
        )

        assert response.status_code == 403, response.text
