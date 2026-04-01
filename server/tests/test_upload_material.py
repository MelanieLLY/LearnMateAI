"""
RED phase tests for POST /api/v1/modules/{module_id}/materials (Upload Material).

These tests are intentionally written BEFORE any implementation exists.
All tests must FAIL at this stage — that is the expected outcome of the RED phase.
"""

from fastapi.testclient import TestClient

BASE_URL = "/api/v1/modules"

def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}

class TestUploadMaterial:
    def test_upload_material_success(self, client: TestClient, instructor_token: str) -> None:
        """Uploading a file returns 201 Created and the material details."""
        # Create a module first
        create_resp = client.post(
            BASE_URL,
            json={"title": "Test Module for Uploads"},
            headers=_auth(instructor_token),
        )
        assert create_resp.status_code == 201
        module_id = create_resp.json()["id"]

        # Upload a dummy file
        files = {"file": ("test.pdf", b"dummy content", "application/pdf")}
        response = client.post(
            f"{BASE_URL}/{module_id}/materials",
            files=files,
            headers=_auth(instructor_token),
        )

        assert response.status_code == 201, response.text
        data = response.json()
        assert "url" in data
        assert data["filename"] == "test.pdf"
        assert "id" in data

    def test_upload_material_not_found(self, client: TestClient, instructor_token: str) -> None:
        """Uploading to a non-existent module returns 404."""
        files = {"file": ("test.pdf", b"dummy content", "application/pdf")}
        response = client.post(
            f"{BASE_URL}/99999/materials",
            files=files,
            headers=_auth(instructor_token),
        )
        assert response.status_code == 404, response.text

    def test_upload_material_unauthenticated(self, client: TestClient) -> None:
        """Uploading without authentication returns 401."""
        files = {"file": ("test.pdf", b"dummy content", "application/pdf")}
        response = client.post(
            f"{BASE_URL}/1/materials",
            files=files,
        )
        assert response.status_code == 401, response.text

    def test_upload_material_student_forbidden(self, client: TestClient, student_token: str) -> None:
        """Uploading as a student returns 403."""
        files = {"file": ("test.pdf", b"dummy content", "application/pdf")}
        response = client.post(
            f"{BASE_URL}/1/materials",
            files=files,
            headers=_auth(student_token),
        )
        assert response.status_code == 403, response.text

    def test_upload_material_missing_file(self, client: TestClient, instructor_token: str) -> None:
        """Uploading without a file payload returns 422."""
        # Create a module first
        create_resp = client.post(
            BASE_URL,
            json={"title": "Test Module for Uploads 2"},
            headers=_auth(instructor_token),
        )
        assert create_resp.status_code == 201
        module_id = create_resp.json()["id"]

        response = client.post(
            f"{BASE_URL}/{module_id}/materials",
            headers=_auth(instructor_token),
        )
        assert response.status_code == 422, response.text
