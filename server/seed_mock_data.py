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
    # Just letters and digits to avoid any parsing/copy issues with special chars
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def run_seed():
    db = SessionLocal()
    credentials = []

    try:
        # Clear existing old notes and enrollments to avoid duplicating when re-running
        db.query(StudentNote).delete()
        db.query(Enrollment).delete()
        
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
            
        credentials.append(f"Instructor 1\n{active_teacher.email}\n{t1_pwd}\n")

        # 2. Add second teacher
        # Check if already exists from previous run
        teacher2 = db.query(User).filter(User.email == "dr.jane.doe@university.edu").first()
        t2_pwd = generate_pwd()
        if teacher2:
            teacher2.hashed_password = get_password_hash(t2_pwd)
        else:
            teacher2 = User(
                email="dr.jane.doe@university.edu",
                full_name="Dr. Jane Doe",
                role="instructor",
                hashed_password=get_password_hash(t2_pwd)
            )
            db.add(teacher2)
        credentials.append(f"Instructor 2\n{teacher2.email}\n{t2_pwd}\n")

        # 3. Add three students
        student_data = [
            ("alex.johnson@student.edu", "Alex Johnson", "Student 1"),
            ("emily.davis@student.edu", "Emily Davis", "Student 2"),
            ("michael.wilson@student.edu", "Michael Wilson", "Student 3")
        ]
        students = []
        for email, name, title in student_data:
            s_pwd = generate_pwd()
            s = db.query(User).filter(User.email == email).first()
            if s:
                s.hashed_password = get_password_hash(s_pwd)
            else:
                s = User(
                    email=email,
                    full_name=name,
                    role="student",
                    hashed_password=get_password_hash(s_pwd)
                )
                db.add(s)
            students.append(s)
            credentials.append(f"{title}\n{email}\n{s_pwd}\n")
            
        # Delete old useless accounts (not matching our preserved/new emails)
        valid_emails = ["robert.smith@university.edu", "dr.jane.doe@university.edu"] + [s[0] for s in student_data]
        useless_users = db.query(User).filter(User.email.notin_(valid_emails)).all()
        for u in useless_users:
            db.delete(u)
            
        db.flush() # flush to get IDs for teacher2 and students

        # 4. Generate new courses and modules (Only create if not exist)
        course_configs = [
            # Title, Instructor
            ("Web开发实践 (Web Development Practice)", active_teacher),
            ("机器学习应用 (ML Applications)", active_teacher),
            ("自然语言处理高级技术 (Advanced NLP)", teacher2),
            ("人机交互设计 (HCI Design)", teacher2)
        ]
        
        module_base_titles = ["基础架构设计", "核心原理解析", "实践案例应用", "进阶难点攻克", "期末复习串讲"]
        
        for c_title, instructor in course_configs:
            c = db.query(Course).filter(Course.title == c_title).first()
            if not c:
                c = Course(title=c_title, description=f"这是一门由教授带领的深度课程，注重动手实践与理论结合。", instructor_id=instructor.id)
                db.add(c)
                db.flush()
                # add modules
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
                    note_sentences = [
                        f"对于【{clean_title}】这一块的知识点我已经理解得很好了，自己动手推导了一遍，考试可以不用再复习这节了。",
                        f"这堂课信息量好大，但是老师讲到【{clean_title}】里面那些底层原理怎么相互呼应的时候，我的脑子一团乱，完全没听懂。",
                        f"今天课上老师特意敲黑板强调了【{clean_title}】在实际应用场景中是重中之重的内容，需要在这个模组上多花时间死磕。"
                    ]
                    sentence = random.choice(note_sentences)
                    note = StudentNote(
                        student_id=s.id,
                        module_id=target_module.id,
                        content=sentence
                    )
                    db.add(note)
                    
        db.commit()
        
        print("Successfully seeded mock data!")
        
        # Write credentials to root
        root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cred_file = os.path.join(root_path, "test_accounts.md")
        with open(cred_file, "w") as f:
            f.write("# Mock Test Accounts\n\n")
            for c in credentials:
                f.write(c + "\n")
        print(f"Saved credentials to {cred_file}")
        
        # Remove old text file if it exists
        old_txt = os.path.join(root_path, "test_accounts.txt")
        if os.path.exists(old_txt):
            os.remove(old_txt)

    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_seed()
