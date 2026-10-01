import os
from dotenv import load_dotenv

load_dotenv()

from src.database import SessionLocal
from src.services.quiz_service import generate_and_store_quiz

db = SessionLocal()
try:
    quiz = generate_and_store_quiz(
        db=db,
        module_id=16,
        student_id=1,
        difficulty_level="Medium",
        num_questions=5,
        is_instructor_assigned=True
    )
    print("SUCCESS: Quiz generated", quiz.id)
except Exception as e:
    import traceback
    traceback.print_exc()
