import pytest
from fastapi.testclient import TestClient
from src.database import get_db
from src.models.module import Module
import json

def test_generate_quiz_instructor(client: TestClient, instructor_token: str, mocker):
    mocker.patch(
        "src.services.quiz_service.generate_quiz",
        return_value={
            "title": "Mock Quiz",
            "difficulty_level": "Medium",
            "questions": [
                {
                    "id": 1,
                    "text": "test?",
                    "question_type": "short_answer",
                    "options": None,
                    "correct_answer": "test",
                    "explanation": "test"
                }
            ]
        }
    )
    # Insert module directly into db mock
    db = next(get_db())
    m = Module(title="Test", description="Test obj", course_id=1, instructor_id=1)
    db.add(m)
    db.commit()
    db.refresh(m)

    response = client.post(
        f"/api/v1/modules/{m.id}/quizzes",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={"difficulty_level": "Medium", "num_questions": 1}
    )
    print("STATUS:", response.status_code)
    print("BODY:", response.text)
    assert response.status_code == 201

