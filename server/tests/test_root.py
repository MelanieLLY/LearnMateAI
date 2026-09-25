"""Tests for the API root endpoint."""

from fastapi.testclient import TestClient


def test_root_returns_status_and_docs_link(client: TestClient) -> None:
    """GET / returns 200 with a status flag and a pointer to the API docs."""
    response = client.get("/")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["docs"] == "/docs"
