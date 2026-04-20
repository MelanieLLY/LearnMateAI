import os
from dotenv import load_dotenv
load_dotenv('.env')  # explicitly load from server/.env

import logging
logging.basicConfig(level=logging.INFO)

from src.database import SessionLocal
from src.services.quiz_service import generate_and_store_quiz
try:
    db = SessionLocal()
    generate_and_store_quiz(db, module_id=1, student_id=1, is_instructor_assigned=True)
    print("SUCCESS")
except Exception as e:
    import traceback
    traceback.print_exc()
