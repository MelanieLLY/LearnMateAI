import os
import random
import string
import sys

# Set up to run from the root of server directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database import SessionLocal, engine, Base
from src.models.user import User
from src.models.course import Course
from src.models.module import Module
from src.models.enrollment import Enrollment
from src.models.student_note import StudentNote
from src.models.quiz import Quiz
from src.models.quiz_submission import QuizSubmission
from src.services.auth_service import get_password_hash

def generate_pwd(length=12):
    # Just letters and digits to avoid any parsing/copy issues with special chars
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

import json

def run_seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    credentials = []

    # Load mock data from JSON
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mock_data.json")
    with open(json_path, "r", encoding="utf-8") as f:
        mock_data = json.load(f)

    # Resolve password placeholders — values in mock_data.json are env var *names*
    # (e.g. "SEED_STUDENT1_PASSWORD"). Substitute from the environment, or fall
    # back to a fresh random password so seeding always succeeds in CI without secrets.
    for entry in mock_data.get("instructors", []) + mock_data.get("students", []):
        placeholder = entry.get("password", "")
        if placeholder and placeholder.isupper() and "_" in placeholder:
            # Looks like an env-var name — resolve it
            entry["password"] = os.environ.get(placeholder, generate_pwd())

    try:
        # Clear existing old data to avoid duplicating when re-running
        db.query(QuizSubmission).delete()
        db.query(Quiz).delete()
        db.query(StudentNote).delete()
        db.query(Enrollment).delete()
        db.query(Module).delete()
        db.query(Course).delete()
        
        instructors_by_email = {}
        students = []

        # 1. Add/Update Instructors
        for inst_data in mock_data["instructors"]:
            inst_email = inst_data["email"]
            inst = db.query(User).filter(User.email == inst_email).first()
            pwd = inst_data.get("password", generate_pwd())
            
            if inst:
                inst.full_name = inst_data["full_name"]
                inst.hashed_password = get_password_hash(pwd)
            else:
                inst = User(
                    email=inst_email,
                    full_name=inst_data["full_name"],
                    role="instructor",
                    hashed_password=get_password_hash(pwd)
                )
                if "id" in inst_data:
                    inst.id = inst_data["id"] 
                db.add(inst)
            
            credentials.append(f"{inst_data['title']}\n{inst_email}\n{pwd}\n")
            instructors_by_email[inst_email] = inst

        db.flush()

        # 2. Add/Update Students
        for stu_data in mock_data["students"]:
            stu_email = stu_data["email"]
            s = db.query(User).filter(User.email == stu_email).first()
            pwd = stu_data.get("password", generate_pwd())
            
            if s:
                s.hashed_password = get_password_hash(pwd)
                s.full_name = stu_data["full_name"]
            else:
                s = User(
                    email=stu_email,
                    full_name=stu_data["full_name"],
                    role="student",
                    hashed_password=get_password_hash(pwd)
                )
                db.add(s)
            
            students.append(s)
            credentials.append(f"{stu_data['title']}\n{stu_email}\n{pwd}\n")

        # Delete old useless accounts
        valid_emails = [i["email"] for i in mock_data["instructors"]] + [s["email"] for s in mock_data["students"]]
        useless_users = db.query(User).filter(User.email.notin_(valid_emails)).all()
        for u in useless_users:
            db.delete(u)
            
        db.flush() # flush to get IDs for students and instructors

        # 3. Generate new courses and modules (Only create if not exist)
        for course_data in mock_data["courses"]:
            c_title = course_data["title"]
            instructor = instructors_by_email[course_data["instructor_email"]]
            description = course_data["description"]
            modules_data = course_data["modules"]
            
            c = db.query(Course).filter(Course.title == c_title).first()
            if not c:
                c = Course(title=c_title, description=description, instructor_id=instructor.id)
                db.add(c)
                db.flush()
                # add modules
                for i, m_data in enumerate(modules_data, start=1):
                    m = Module(
                        course_id=c.id,
                        title=f"{c.title.split(' ')[0]} - Module {i}: {m_data['title']}",
                        description=m_data['desc'],
                        instructor_id=c.instructor_id,
                        learning_objectives="Deeply understand and master core technologies",
                    )
                    db.add(m)
        db.flush()

        all_courses = db.query(Course).all()

        # 5. Enrollments & Notes
        for s in students:
            for c in all_courses:
                # Enroll
                enroll = Enrollment(student_id=s.id, course_id=c.id)
                db.add(enroll)
                
                # Notes 
                # Pick a module from this course
                course_modules = db.query(Module).filter(Module.course_id == c.id).all()
                if course_modules:
                    target_module = random.choice(course_modules)
                    clean_title = target_module.title.split(': ')[-1] if ': ' in target_module.title else target_module.title
                    note_templates = mock_data.get("note_templates", [
                        "I have perfectly mastered the contents of [{clean_title}].",
                        "This is too complex, I didn't understand the underlying principles of [{clean_title}] at all.",
                        "The instructor heavily emphasized that [{clean_title}] is critical, I must review it."
                    ])
                    sentence = random.choice(note_templates).replace("{clean_title}", clean_title)
                    note = StudentNote(
                        student_id=s.id,
                        module_id=target_module.id,
                        content=sentence
                    )
                    db.add(note)
                    
        db.flush()
        
        # 6. Generate Quizzes and Submissions
        print("Generating mock quizzes and submissions...")
        for c in all_courses:
            course_modules = db.query(Module).filter(Module.course_id == c.id).all()
            for m in course_modules:
                # Create a generic Instructor-assigned quiz for this module
                quiz = Quiz(
                    title=f"Assessment: {m.title}",
                    difficulty_level="Medium",
                    questions=[{"id": 1, "text": "Mock Question?", "question_type": "short_answer", "correct_answer": "42", "explanation": "Mock"}],
                    module_id=m.id,
                    student_id=c.instructor_id, # use instructor's ID to denote assigned quiz
                    is_instructor_assigned=True
                )
                db.add(quiz)
                db.flush()
                
                # Each student submits it
                for s in students:
                    score = random.randint(50, 100)
                    sub = QuizSubmission(
                        quiz_id=quiz.id,
                        student_id=s.id,
                        score=score
                    )
                    db.add(sub)
                    
        db.commit()
        
        print("Successfully seeded mock data!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_seed()
