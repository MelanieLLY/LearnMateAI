from fastapi.testclient import TestClient
from src.main import app
from src.schemas.quiz import QuizResponse
from src.services.quiz_service import generate_and_store_quiz
from src.database import SessionLocal
import os

from dotenv import load_dotenv
load_dotenv('.env')

db = SessionLocal()
quiz = generate_and_store_quiz(db, module_id=1, student_id=1, is_instructor_assigned=True)

try:
    print("Validating into Pydantic...")
    res = QuizResponse.model_validate(quiz)
    print("Success. Passed validation.")
except Exception as e:
    import traceback
    traceback.print_exc()

