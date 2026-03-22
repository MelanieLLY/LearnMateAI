"""
RED phase tests for DELETE /api/v1/modules/{module_id} (Delete Module).

These tests are intentionally written BEFORE any implementation exists.
All tests must FAIL at this stage — that is the expected outcome of the RED phase.

Helper
------
``_auth(token)`` — builds the Authorization header dict to keep test bodies concise.
``_create_module(...)`` — creates a module via the existing POST endpoint and returns its id.

Covered scenarios
-----------------
1. Happy Path      : owner deletes their module              → 204 No Content; row is gone
2. Not Found       : delete a module_id that never existed   → 404 with "module" in detail
3. Unauthenticated : no Authorization header                 → 401 Unauthorized
4. Wrong Role      : valid token but role='student'          → 403 Forbidden
5. Wrong Owner     : different instructor tries to delete     → 403 Forbidden
"""

from fastapi.testclient import TestClient

BASE_URL = "/api/v1/modules"


def _auth(token: str) -> dict:
    """Return an Authorization header dict for the given Bearer token."""
    return {"Authorization": f"Bearer {token}"}


def _create_module(client: TestClient, token: str, title: str) -> int:
    """Create a module via POST and return its id.  Asserts 201 so setup failures are obvious."""
    resp = client.post(BASE_URL, json={"title": title, "description": "desc"}, headers=_auth(token))
    assert resp.status_code == 201, f"Setup failed creating module: {resp.text}"
    return resp.json()["id"]


class TestDeleteModule:
    """Test suite for the Delete Module API endpoint (DELETE /api/v1/modules/{module_id})."""

    # ------------------------------------------------------------------
    # 1. Happy Path
    # ------------------------------------------------------------------

    def test_delete_module_success(self, client: TestClient, instructor_token: str) -> None:
        """Owner deletes their module → 204 No Content; the row is confirmed gone.

        After the 204 response, a second DELETE on the same id must return 404,
        proving the row was actually removed from the database and not merely
        soft-deleted or left in place.
        """
        module_id = _create_module(client, instructor_token, "Module To Delete")

        response = client.delete(
            f"{BASE_URL}/{module_id}",
            headers=_auth(instructor_token),
        )

        assert response.status_code == 204, response.text
        assert response.content == b"", "204 response body must be empty"

        # Verify the row is truly gone by attempting a second delete.
        follow_up = client.delete(
            f"{BASE_URL}/{module_id}",
            headers=_auth(instructor_token),
        )
        assert follow_up.status_code == 404, follow_up.text

    # ------------------------------------------------------------------
    # 2. Not Found
    # ------------------------------------------------------------------

    def test_delete_module_not_found(self, client: TestClient, instructor_token: str) -> None:
        """Deleting a non-existent module_id returns 404 with a meaningful detail message.

        The detail must contain "module" to prove a real DB lookup occurred,
        not just FastAPI's generic route-missing 404 {"detail": "Not Found"}.
        """
        response = client.delete(
            f"{BASE_URL}/99999",
            headers=_auth(instructor_token),
        )

        assert response.status_code == 404, response.text
        assert "module" in response.json()["detail"].lower()

    # ------------------------------------------------------------------
    # 3. Unauthenticated
    # ------------------------------------------------------------------

    def test_delete_module_unauthenticated(self, client: TestClient) -> None:
        """A request with no Authorization header returns 401 Unauthorized."""
        response = client.delete(f"{BASE_URL}/1")

        assert response.status_code == 401, response.text

    # ------------------------------------------------------------------
    # 4. Wrong Role (student cannot delete modules)
    # ------------------------------------------------------------------

    def test_delete_module_student_role_forbidden(
        self, client: TestClient, student_token: str
    ) -> None:
        """A request authenticated as a student returns 403 Forbidden."""
        response = client.delete(
            f"{BASE_URL}/1",
            headers=_auth(student_token),
        )

        assert response.status_code == 403, response.text

    # ------------------------------------------------------------------
    # 5. Wrong Owner (different instructor cannot delete another's module)
    # ------------------------------------------------------------------

    def test_delete_module_wrong_instructor(
        self,
        client: TestClient,
        instructor_token: str,
        second_instructor_token: str,
    ) -> None:
        """Instructor 2 cannot delete a module owned by Instructor 1 → 403 Forbidden.

        This enforces that ownership is verified before deletion, not just the role.
        """
        module_id = _create_module(client, instructor_token, "Owned By Instructor 1")

        response = client.delete(
            f"{BASE_URL}/{module_id}",
            headers=_auth(second_instructor_token),
        )

        assert response.status_code == 403, response.text
