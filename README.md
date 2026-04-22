(/init demonstration for HW5 grading purpose)

<img width="800" alt="init" src="https://github.com/user-attachments/assets/cd358470-668c-4226-8a37-af7739b2b528" />

<img width="800" alt="init2" src="https://github.com/user-attachments/assets/502f65f4-c737-4121-a22c-42fa8c3fd00e" />

below is the start of the readme for project 3

----------------

# LearnMate AI

LearnMate AI is a smart teaching assistant platform made for modern schools. It has different parts for instructors and students. We built this to show how to quickly create a production-ready SaaS app using advanced AI coding tools (Claude Code), Agent workflows, and full-stack automatic deployments.

## Blog Post

https://dev.to/jing_2026/learnmateai-building-an-intelligent-teaching-assistant-platform-48pb

https://www.melanieyang.info/post/building-learnmate-ai-engineering-practices-for-a-full-stack-educational-platform-with-claude-code

### Reflection
- Liuyi: [docs/P3_Reflection_Liuyi.md](docs/P3_Reflection_Liuyi.md)
- Jing: [docs/REFLECTION_byJing.md](docs/REFLECTION_byJing.md)

## 📍 Online Demo

> https://youtu.be/LnycwzdsHaU?si=KXOfvtXoiGWtFFuN
> **Network Latency (Cold Start) Note**  
> We use Render's free tier for our backend. If nobody uses the app for a while, the server goes to sleep to save money. So, **your first login might take about 3 minutes to load**. This is normal. Please wait while it wakes up. After that, it will be fast!

* **Frontend (Vercel)**: [https://learn-mate-ai-zeta.vercel.app](https://learn-mate-ai-zeta.vercel.app)
* **Backend (Render)**: [https://learnmate-api.onrender.com](https://learnmate-api.onrender.com)

### 🔑 Test Accounts

You can try the app easily using these test accounts:

**👨‍🏫 Instructor Role**
* **Account**: `robert.smith@university.edu`
* **Password**: `owEuWEmcl2Xx`

**🎓 Student Role**
* **Account (Student A)**: `alex.johnson@student.edu`
* **Password**: `dUfkhVsX8vJQ`
* **Account (Student B)**: `emily.davis@student.edu`
* **Password**: `OKmjlTF25O2r`

---

## 🚀 Core Features & Smart Designs

We did not want to make a simple CRUD app. Instead, we created special features to solve real problems in education:

### 1. Instructor Features
* **Safe Content Control**
  * **Design**: To stop the AI from generating harmful or biased content, instructors can set an "audience profile" for the class. The Prompt Engine uses this profile to make sure the AI respects cultural and psychological safety.
* **Live Class Report Dashboard** 
  * **Design**: Instead of boring tables, our dashboard calculates class averages in real time. It uses backend QuizSubmission data to show an "Error Distribution Radar." This helps instructors see what the class is struggling with without breaking student privacy.

### 2. Student Features
* **Interactive 3D Flashcards**
  * **Design**: Reading long texts is tiring. We used CSS3 to build real-feeling 3D flipping flashcards. The LLM summarizes long PDFs into these fun, pocket-sized cards.
* **Smart Quizzes with Helpful Feedback**
  * **Design**: We used a step-by-step layout for taking quizzes. When you finish, the LLM API quickly gives you a Score Badge and deep feedback on your mistakes. It feels like a real tutor is grading your test.

### 3. Setup & Security
* **Data Safety by Role**
  * **Design**: We use React Context and strict router rules so that students and instructors can only see their own data. This completely blocks accounts from seeing data they shouldn't.

---

## 🏗 System Architecture

The app is built to handle many users, keep data safe, and connect securely with APIs:

<img alt="System Architecture Diagram" src="https://github.com/user-attachments/assets/45ff7555-95a6-45f3-b1df-ec1d5fa6b91f" />

<br/>

<details>
<summary><h3> 📊 Click here to expand Mermaid Source Code</h3></summary>

<br/>

```mermaid
graph TD
    %% Client and UI Layer
    subgraph Client [Frontend: Vite / React]
        direction LR
        UI[UI Components<br/>Tailwind CSS] --- Router[React Router<br/>Navigation]
        Router --- APIStore[State & API<br/>Data Fetching]
    end

    %% Backend and API Layer
    subgraph Server [Backend: FastAPI / Python]
        direction LR
        Security[JWT Auth<br/>Security] --- API[FastAPI<br/>Endpoints]
        API --- Handlers[Business<br/>Logic / Handlers]
        Handlers --- Prompt[Prompt<br/>Engine / LLM]
    end

    %% Infrastructure & LLM Integration
    subgraph Infrastructure [Cloud Infrastructure]
        direction LR
        DB[(PostgreSQL<br/>Cloud Database)]
        LLM[OpenAI /<br/>Anthropic APIs]
    end

    %% Relations
    APIStore -- "Axios HTTP Request" --> API
    API -. "JSON Response" .-> APIStore
    Handlers -- "SQLAlchemy ORM" --> DB
    Prompt -- "LLM Reasoning & Tool Calls" --> LLM
```

</details>

---

## 🛠 Tech Stack

* **Frontend**: React.js 18, Vite, React Router DOM, Tailwind CSS (with Skeleton loading)
* **Backend**: Python 3.10+, FastAPI, Pydantic, SQLAlchemy ORM
* **Database**: PostgreSQL Cloud (Neon/Render DB)
* **CI/CD Pipeline**: GitHub Actions
* **Quality & Security**: ESLint, Flake8, Gitleaks, Bandit, NPM Audit

---

## 🤖 Claude Code & Workflow

A big highlight of this project is how we used AI to build it, following the Project 3 Guidelines:

1. **Test-Driven Development (TDD)**
   * To stop AI mistakes, we used Pytest integration loops. This forces the model to follow Pydantic Schemas exactly.
2. **AI Agent Environment (`.claude`)**
   * The project has special prompt rules in `CLAUDE.md`. We also set up a custom Git hook that stops developers from pushing code if tests fail. This keeps the code high quality.
3. **Security & CI/CD Pipeline**
   * Our 9-stage CI pipeline checks for secrets (Gitleaks), deploys the code, and runs AI Code Reviews automatically on the master branch.

---

## 💻 Local Development Setup

To run this app on your computer:

```bash
# 1. Download the code (Look at .env.example for variables)
git clone <repository-url>
cd LearnMateAI

# 2. Start the frontend (Port: 5200)
cd client
npm install
npm run dev

# 3. Start the backend API (Port: 8200)
cd server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8200
```

---

## License & Project Info

**Copyright © 2026 LearnMate Team. All Rights Reserved.**

This repository is an academic project for grading in Project 3. You may not copy, share, or sell this code. 

> **Visual Drafts:**
> Early design screenshots from the `/init` sprint:
> [Draft 1](https://github.com/user-attachments/assets/cd358470-668c-4226-8a37-af7739b2b528) | [Draft 2](https://github.com/user-attachments/assets/502f65f4-c737-4121-a22c-42fa8c3fd00e)

---

## 📑 Project 3 Evidence & Requirement Mapping

| Requirement Category | Implementation & Completion Details | Evidence File / Link |
|----------------------|-------------------------------------|----------------------|
| **CLAUDE.md & Memory** | Created a comprehensive `CLAUDE.md` with modular `@imports`. Auto-memory is tracked in `chathistory_P3.md` and project Git logs show iterative evolution. | [chathistory_P3.md](planning_files/chathistory_P3.md) <br> [CLAUDE.md](CLAUDE.md) |
| **Custom Skills** | Integrated `everything-claude-code` plugin, establishing minimum 2 custom skills (`tdd-workflow`, `add-feature-skill` etc.). | [Evidence 1 (Screenshot)](docs/screenshot/12_evidence_1_successfully_add_marketplace_proof.png) |
| **Hooks** | Configured automated Pre/Post hooks. Specifically implemented a Stop hook that runs tests and blocks `git commit` if the Pytest suite fails. | [Evidence 2 (Screenshot)](docs/screenshot/13_evidence_2_stop_hook.png) |
| **MCP Servers** | Added and configured the GitHub MCP server to securely fetch issues and interact with the repository, stored in `.mcp.json`. | [Evidence 4 (Screenshot)](docs/screenshot/15_evidence_4_mcp_open_issues.png) |
| **Agents** | Applied the Agent SDK and implemented specialized agents like the Doc-Reviewer agent to actively assist in professional workflows. | [Evidence 3 (Screenshot)](docs/screenshot/14_evidence_3_doc_reviewer_agent.png) <br> [project3-agents.md](docs/project3-agents.md) |
| **Parallel Development** | Split our repository into separate Git worktrees (`quiz-ui` and `flashcard-ui`), building distinct features simultaneously across two terminals. | [Evidence 5 (Screenshot)](docs/screenshot/16_evidence_5_worktree_list.png) <br> [Evidence 7b (Screenshot)](docs/screenshot/17_evidence_7b_parallel_terminals.png) |
| **Writer/Reviewer + C.L.E.A.R.** | AI acted as writer, while the autonomous Code-Reviewer agent performed PR evaluations following the exact C.L.E.A.R framework guidelines. | [Evidence 8: PR 36 Review](docs/screenshot/21_clear_pr_36_review.png) <br> [Evidence 8: PR 37 Review](docs/screenshot/22_clear_pr_37_review.png) <br> [Evidence 10: PR 20 Review](docs/screenshot/20_evidence_10_clear_pr_comment.png) |
| **Test-Driven Development** | Fully integrated the Red-Green-Refactor loop. We committed failing tests first, followed by passing solutions, achieving >70% coverage. | [Evidence 6 (RED phase)](docs/screenshot/01_RED_phase_failing_tests.png) <br> [Evidence 7 (GREEN phase)](docs/screenshot/02_01_GREEN_phase_passed.png) <br> [Evidence 11 (E2E)](docs/screenshot/18_evidence_11_playwright_e2e_report.png) |
| **CI/CD Pipeline & Security** | Automated a 9-stage GitHub Actions workflow encompassing linting, testing, security scans (npm audit, Gitleaks, Bandit), and Vercel deployments. | [Evidence 9 (CI Green)](docs/screenshot/19_evidence_9_github_actions_all_green.png) <br> [Evidence 12 (PR checks)](docs/screenshot/22_evidence_12_github_actions_pr.gif) |
| **Team Process** | Documented sprint plans natively. Adopted a strict branch-per-issue workflow managed via GitHub issues and asynchronous standups. | [learnmate-sprint-plan.md](docs/learnmate-sprint-plan.md) |
| **Usability Study** | Conducted usability testing on the platform involving both Student and Instructor personas. | [Report](docs/Usability_Study_Report.md) <br> [General Video](docs/instructor%20general%20usability%20video.mov) <br> [Quiz Video](docs/instructor%20create%20quiz%20usability%20video.mov) |
| **Application Quality & Deployment** | A polished, production-ready SaaS application featuring dynamic dual-role dashboards, fully deployed with the frontend on Vercel and backend on Render. | [Vercel App](https://learn-mate-ai-zeta.vercel.app) <br> [Render API](https://learnmate-api.onrender.com) |
| **Technical Blog Post** | Published comprehensive technical blogs on external platforms, unpacking the architectural decisions and how Claude Code accelerated the agile sprints. | [Blog (Melanie)](https://www.melanieyang.info/post/building-learnmate-ai-engineering-practices-for-a-full-stack-educational-platform-with-claude-code) <br> [Blog (Jing)](https://dev.to/jing_2026/learnmateai-building-an-intelligent-teaching-assistant-platform-48pb) |
| **Individual Reflections** | Prepared in-depth 500+ word reflections summarizing personal takeaways, challenges overcome, and experiences with Claude Code's Hooks, MCP, and Agent workflows. | [Reflection (Liuyi)](docs/P3_Reflection_Liuyi.md) <br> [Reflection (Jing)](docs/REFLECTION_byJing.md) |
| **Peer Review** | Provided a professional peer review document summarizing Jing's contributions and collaboration throughout the project lifecycle. | [Peer Review (Jing)](docs/Peer_Review_Liuyi_to_Jing.md) |
| **Video Demonstration** | A comprehensive screencast walkthrough demonstrating the app's core functionalities alongside the AI-assisted workflows (TDD, Hooks, etc.). | https://youtu.be/LnycwzdsHaU?si=KXOfvtXoiGWtFFuN |
| **Showcase Submission** | Compiled all final project assets including URLs, thumbnails, and documentation into the course's official Google Form. | `Submitted via Google Form` |
