from src.database import SessionLocal
from src.models.quiz import Quiz
from src.schemas.quiz import QuizResponse

db = SessionLocal()
quiz = db.query(Quiz).order_by(Quiz.id.desc()).first()
try:
    resp = QuizResponse.model_validate(quiz)
    print("SUCCESS:", resp.title)
except Exception as e:
    print("ERROR:", e)
