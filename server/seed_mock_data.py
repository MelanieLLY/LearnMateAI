import os
import random
import string
import sys

# Set up to run from the root of server directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database import SessionLocal
from src.models.user import User
from src.models.course import Course
from src.models.module import Module
from src.models.enrollment import Enrollment
from src.models.student_note import StudentNote
from src.services.auth_service import get_password_hash

def generate_pwd(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

def run_seed():
    db = SessionLocal()
    credentials = []

    try:
        # 1. Update existing teacher (id=1)
        active_teacher = db.query(User).filter(User.id == 1).first()
        t1_pwd = generate_pwd()
        
        if active_teacher:
            active_teacher.email = "robert.smith@university.edu"
            active_teacher.full_name = "Prof. Robert Smith"
            active_teacher.hashed_password = get_password_hash(t1_pwd)
        else:
            print("Active teacher id=1 not found! Creating...")
            active_teacher = User(
                id=1, email="robert.smith@university.edu", 
                full_name="Prof. Robert Smith", role="instructor",
                hashed_password=get_password_hash(t1_pwd)
            )
            db.add(active_teacher)
            
        credentials.append(f"Instructor 1: {active_teacher.email} / {t1_pwd}")

        # 2. Add second teacher
        t2_pwd = generate_pwd()
        teacher2 = User(
            email="dr.jane.doe@university.edu",
            full_name="Dr. Jane Doe",
            role="instructor",
            hashed_password=get_password_hash(t2_pwd)
        )
        db.add(teacher2)
        credentials.append(f"Instructor 2: {teacher2.email} / {t2_pwd}")

        # 3. Add three students
        student_data = [
            ("alex.johnson@student.edu", "Alex Johnson"),
            ("emily.davis@student.edu", "Emily Davis"),
            ("michael.wilson@student.edu", "Michael Wilson")
        ]
        students = []
        for email, name in student_data:
            s_pwd = generate_pwd()
            s = User(
                email=email,
                full_name=name,
                role="student",
                hashed_password=get_password_hash(s_pwd)
            )
            db.add(s)
            students.append(s)
            credentials.append(f"Student: {email} / {s_pwd}")
            
        # Delete old useless accounts (not matching our preserved/new emails)
        valid_emails = ["robert.smith@university.edu", "dr.jane.doe@university.edu"] + [s[0] for s in student_data]
        useless_users = db.query(User).filter(User.email.notin_(valid_emails)).all()
        for u in useless_users:
            db.delete(u)
            
        db.flush() # flush to get IDs for teacher2 and students

        # 4. Generate new courses and modules
        course_configs = [
            # Title, Instructor
            ("Web开发实践 (Web Development Practice)", active_teacher),
            ("机器学习应用 (ML Applications)", active_teacher),
            ("自然语言处理高级技术 (Advanced NLP)", teacher2),
            ("人机交互设计 (HCI Design)", teacher2)
        ]
        
        new_courses = []
        for c_title, instructor in course_configs:
            c = Course(title=c_title, description="这是一门由资深教授带领的深度课程，注重动手实践与理论结合。", instructor_id=instructor.id)
            db.add(c)
            new_courses.append(c)
        db.flush()

        module_base_titles = ["基础架构设计", "核心原理解析", "实践案例应用", "进阶难点攻克", "期末复习串讲"]
        
        all_courses = db.query(Course).all() # This inherently includes the existing CS7180
        
        for idx, c in enumerate(new_courses):
            # Create 5 modules for EACH new course
            for i, m_title in enumerate(module_base_titles, start=1):
                m = Module(
                    course_id=c.id,
                    title=f"{c.title.split(' ')[0]} - 模组 {i}: {m_title}",
                    description=f"这是【{c.title}】的第{i}章内容。本章将详细讲解{m_title}相关的核心知识，并配备相关实验进行巩固。",
                    instructor_id=c.instructor_id,
                    learning_objectives="深入理解与掌握核心技术",
                )
                db.add(m)
        db.flush()

        # 5. Enrollments & Notes
        # We need the real modules for notes
        note_sentences = [
            "这个知识点我已经理解得很好了，不需要再考了。",
            "这里当时老师讲的时候我没听懂。",
            "老师特意强调了并发编程是重点内容。"
        ]
        
        for s in students:
            for c in all_courses:
                # Enroll
                enroll = Enrollment(student_id=s.id, course_id=c.id)
                db.add(enroll)
                
                # Notes 
                # Pick a module from this course
                course_modules = db.query(Module).filter(Module.course_id == c.id).all()
                if course_modules:
                    target_module = course_modules[0]
                    sentence = random.choice(note_sentences)
                    note = StudentNote(
                        student_id=s.id,
                        module_id=target_module.id,
                        content=f"今天学习了这节课，总体感觉收获很大。{sentence} 感谢AI的辅助功能让我更好地掌握知识结构。"
                    )
                    db.add(note)
                    
        db.commit()
        
        print("Successfully seeded mock data!")
        
        # Write credentials to root
        root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cred_file = os.path.join(root_path, "test_accounts.txt")
        with open(cred_file, "w") as f:
            f.write("=== Mock Test Accounts ===\n")
            for c in credentials:
                f.write(c + "\n")
        print(f"Saved credentials to {cred_file}")

    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_seed()
