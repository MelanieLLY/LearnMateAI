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
        # Clear existing old data to avoid duplicating when re-running
        db.query(StudentNote).delete()
        db.query(Enrollment).delete()
        db.query(Module).delete()
        db.query(Course).delete()
        
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
        course_configs = {
            "Web开发实践 (Web Development Practice)": {
                "instructor": active_teacher,
                "description": "本课程旨在介绍现代Web开发的基础理论与实践技术，涵盖前端技术栈（如React/Vue）与后端服务框架及数据库集成，强调通过实际项目培养全栈开发能力。",
                "modules": [
                    {"title": "Web基础与前端框架", "desc": "学习HTML semantics, CSS3高级布局，并深入React生态，掌握组件化开发思想。"},
                    {"title": "后端架构设计", "desc": "探索RESTful API设计与GraphQL架构，学习如何利用Node.js或Python FastAPI构建高并发的后端服务。"},
                    {"title": "数据库集成与运维", "desc": "深入讲解NoSQL与关系型数据库设计，并介绍Docker容器化部署。"},
                    {"title": "全栈项目实战", "desc": "独立完成一个包含前后端交互、身份验证与数据持久化的完整企业级Web应用。"},
                    {"title": "性能优化与测试", "desc": "掌握前端渲染优化、后端缓存策略，并编写高覆盖率的单元测试与端到端测试。"}
                ]
            },
            "机器学习应用 (ML Applications)": {
                "instructor": active_teacher,
                "description": "这是一门侧重于将机器学习算法运用到实际工业场景的课程，涵盖数据工程、模型训练、评估及模型部署，帮助学生掌握完整的ML生命周期。",
                "modules": [
                    {"title": "数据预处理与特征工程", "desc": "掌握数据清洗、缺失值处理、特征提取及降维技术的核心方法论。"},
                    {"title": "监督学习算法应用", "desc": "深入探讨逻辑回归、支持向量机及各种集成学习模型的实际应用案例。"},
                    {"title": "深度学习实战入门", "desc": "学习利用PyTorch构建基本的前馈神经网络与卷积神经网络，并了解如何进行超参数调优。"},
                    {"title": "模型评估与诊断", "desc": "如何通过交叉验证、混淆矩阵、ROC曲线等指标全面诊断模型的偏差与方差问题。"},
                    {"title": "模型部署与监控", "desc": "利用Flask/FastAPI开发模型推理服务，并学习使用MLOps工具对线上模型运行状态进行监控。"}
                ]
            },
            "自然语言处理高级技术 (Advanced NLP)": {
                "instructor": teacher2,
                "description": "针对具有一定AI基础的学生，本课程深入剖析自然语言处理的前沿技术，包括Transformer架构、预训练大模型及复杂语言任务的微调方法。",
                "modules": [
                    {"title": "语言模型与注意力机制", "desc": "从RNN回顾到自注意力机制的演进，深入解读Transformer架构的基本原理与计算图。"},
                    {"title": "预训练模型剖析", "desc": "全面解析BERT、GPT模型的底层架构，探讨其在预训练阶段的数据构建与目标函数设计。"},
                    {"title": "大模型微调技术", "desc": "学习通过LoRA、P-Tuning等参数高效的微调方法，对大体量模型进行下游任务适配。"},
                    {"title": "文本生成与信息检索", "desc": "探讨束搜索算法与RAG（检索增强生成）系统，如何解决文本生成的幻觉问题。"},
                    {"title": "NLP前沿论文精读", "desc": "结合最新的顶级会议（ACL/EMNLP）论文，分析多模态交互与模型对齐技术的未来发展路径。"}
                ]
            },
            "人机交互设计 (HCI Design)": {
                "instructor": teacher2,
                "description": "探索人类与计算系统交互的原则。课程将教授从用户调研、原型设计、可用性测试到最终高保真交互落地的完整UX设计流程。",
                "modules": [
                    {"title": "人类认知与界面心理学", "desc": "从人类视觉、记忆与注意力角度，理解这些认知限制如何影响界面元素的设计规范。"},
                    {"title": "用户研究方法", "desc": "学习如何进行定性访谈、发放问卷以及构建详实的用户画像和同理心地图。"},
                    {"title": "信息架构与交互流程", "desc": "运用卡片分类法梳理复杂的系统层级，并建立清晰流畅的用户旅程与操作流程图。"},
                    {"title": "低保真与高保真原型", "desc": "熟练掌握Figma等工具，从线框图过渡到具备复杂动效和微交互的高保真原型。"},
                    {"title": "可用性评估与数据追踪", "desc": "设计并执行A/B测试与可用性测试，并学会在界面迭代中利用定量数据进行决策支撑。"}
                ]
            }
        }
        
        for c_title, config in course_configs.items():
            instructor = config["instructor"]
            description = config["description"]
            modules_data = config["modules"]
            
            c = db.query(Course).filter(Course.title == c_title).first()
            if not c:
                c = Course(title=c_title, description=description, instructor_id=instructor.id)
                db.add(c)
                db.flush()
                # add modules
                for i, m_data in enumerate(modules_data, start=1):
                    m = Module(
                        course_id=c.id,
                        title=f"{c.title.split(' ')[0]} - 模组 {i}: {m_data['title']}",
                        description=m_data['desc'],
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
