"""Tests for the quiz CRUD endpoints."""

import pytest
from fastapi.testclient import TestClient


def test_get_module_quizzes_unauthenticated(client: TestClient) -> None:
    response = client.get("/api/v1/modules/1/quizzes")
    assert response.status_code == 401

def test_get_quiz_unauthenticated(client: TestClient) -> None:
    response = client.get("/api/v1/quizzes/1")
    assert response.status_code == 401

def test_put_quiz_unauthenticated(client: TestClient) -> None:
    response = client.put(
        "/api/v1/quizzes/1",
        json={"title": "Updated Title", "questions": []}
    )
    assert response.status_code == 401

def test_put_quiz_student_forbidden(client: TestClient, student_token: str) -> None:
    response = client.put(
        "/api/v1/quizzes/1",
        headers={"Authorization": f"Bearer {student_token}"},
        json={"title": "Updated Title", "questions": []}
    )
    assert response.status_code == 403

def test_get_quiz_not_found(client: TestClient, student_token: str) -> None:
    response = client.get(
        "/api/v1/quizzes/9999",
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == 404

def test_put_quiz_not_found(client: TestClient, instructor_token: str) -> None:
    response = client.put(
        "/api/v1/quizzes/9999",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={"title": "Updated", "questions": []}
    )
    assert response.status_code == 404
