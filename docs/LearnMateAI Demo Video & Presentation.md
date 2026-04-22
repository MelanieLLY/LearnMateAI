
### 1. Introduction

  - Project Name: LearnMateAI
  - Team Members: Liuyi & Jing

  - ![Student Dashboard Home](docs/screenshot/26_student_dashboard_home.png)

### 2. Project Overview & The Problem

  - Problem: Scattered learning resources, lack of automated study tools.
  - Solution: AI-generated flashcards, summaries, and quizzes; dynamic instructor dashboard.
  - Deployed Link: Show public Vercel URL.

  - ![Vercel Frontend Deploy](docs/screenshot/25_evidence_16_vercel_frontend_deploy.png)
  - ![Render Backend Deploy](docs/screenshot/24_evidence_15_render_backend_deploy.png)

### 3. System Architecture

  - Separated Frontend and Backend design.
  - Tech Stack: React, Vite, FastAPI, PostgreSQL, GitHub Actions, Vercel, Render.

  - <img alt="System Architecture Diagram" src="https://github.com/user-attachments/assets/45ff7555-95a6-45f3-b1df-ec1d5fa6b91f" width="600" />
  - ![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB) ![Vite](https://img.shields.io/badge/Vite-B73BFE?style=flat&logo=vite&logoColor=FFD62E) ![FastAPI](https://img.shields.io/badge/fastapi-109989?style=flat&logo=FASTAPI&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat&logo=github-actions&logoColor=white) ![Vercel](https://img.shields.io/badge/Vercel-000000?style=flat&logo=vercel&logoColor=white) ![Render](https://img.shields.io/badge/Render-46E3B7?style=flat&logo=render&logoColor=white)

### 4. Backend AI Agents & TDD

  - Test-Driven Development (TDD) workflow demonstration (Failing RED tests -> Passing GREEN tests).
  - Agent SDK code implementation.

  - ![Terminal TDD Test Screenshot](docs/screenshot/01_RED_phase_failing_tests.png)
  - ![Agent SDK Code Snippet](https://github.com/user-attachments/assets/e6a8983e-13e3-437e-a25f-5233e896c3b6)

### 5. Frontend UI & Parallel Development

  - Parallel development of UI components using `git worktree`.
  - Interactive quiz and 3D flashcards.
 ![Parallel Git Worktree Terminals](docs/screenshot/17_evidence_7b_parallel_terminals.png)

### 6. Live Demo: Instructor Dashboard

  - Instructor Login -> View Class Average and Module Trends.

  - ![Instructor Dashboard](docs/screenshot/21_instructor_dashboard.gif)
### 7. Live Demo: Student Experience

  - Student Login -> Browse Modules -> Flip 3D Flashcards -> Complete Quiz & AI Feedback.

  - ![Student UI Experience](docs/screenshot/23_student_ui_experience.gif)


### 8. Playwright E2E Testing

  - Automated end-to-end browser test run results.

  - ![Playwright E2E Test All Green](docs/screenshot/18_evidence_11_playwright_e2e_report.png)

### 9. CI/CD Pipeline & Security Gates

  - 9-stage GitHub Actions workflow.
  - Security Checks: Gitleaks, npm audit, Bandit.

  - ![GitHub Actions Workflow All Green](docs/screenshot/19_evidence_9_github_actions_all_green.png)
  - ![GitHub PR Checks All Green](docs/screenshot/22_evidence_12_github_actions_pr.gif)

### 10. Claude Code Mastery

  - Custom Skills for accelerated workflows.
  - PreToolUse Stop hook (blocking unqualified commits).
  - GitHub MCP server connection.
  - AI Code Reviewer Agent based on the C.L.E.A.R. framework.

  - ![Stop Hook Blocking Commit](docs/screenshot/13_evidence_2_stop_hook.png)
  - ![AI Code Review PR Screenshot](docs/screenshot/20_evidence_10_clear_pr_comment.png)

### 11. Conclusion

  - Core Highlights: Production Ready, Robust AI Workflow, Automated Security.

---
<br><br><br><br><br><br><br><br><br><br>
*(Scroll down to view speaker scripts)*
---

## 🎙️ Scripts (For Presentation)

### 🔴 1. Introduction
**Jing (0:15)**: 
> "Hello everyone, welcome to our Project 3 demonstration. We are excited to present LearnMateAI, a production-grade educational application built with Claude Code. I am Jing, and my primary focus was on the backend architecture, generative AI Agent integration, CI/CD security pipelines, and Test-Driven Development (TDD)."

**Liuyi (0:15)**: 
> "I am Liuyi. I was responsible for the frontend UI and interaction design, Playwright end-to-end testing, and the CI/CD deployment logic on Render and Vercel. I also configured core Claude Code tools such as Hooks and MCP."

### 🔴 2. Project Overview & The Problem
**Liuyi (0:30)**: 
> "LearnMateAI addresses the lack of automated, interactive learning resources. Our platform allows instructors to generate learning materials like 3D flashcards and quizzes instantly, while tracking student performance in real time. The application is fully deployed and accessible via our public URL."

### 🔴 3. System Architecture
**Liuyi (0:25)**: 
> "Our system architecture strictly separates the frontend and backend. The client interface uses React and Vite, communicating with a Python FastAPI backend. Our data is stored in a PostgreSQL database hosted on Render, and the frontend is deployed via Vercel."

### 🔴 4. Backend AI Agents & TDD
**Jing (0:45)**: 
> "For the core backend services, we strictly followed a Test-Driven Development (TDD) workflow. As shown in the Git history, I consistently wrote and committed failing unit tests before implementing the APIs to pass them. To handle our generative AI requirements, I built three distinct Agent SDK functions to generate course summaries, flashcards, and quizzes. This ensures the reliability of the generated content, which is thoroughly covered by our 96 Pytest test cases."

### 🔴 5. Frontend UI & Parallel Development
**Liuyi (0:30)**: 
> "Concurrent with the backend development, we utilized Git Worktrees to enable parallel development within the same repository. I ran multiple terminal sessions, building the interactive quiz UI in one worktree and the 3D flashcard UI in another. This completely isolated our work and allowed us to iterate on the UI quickly without Git conflicts."

### 🔴 6. Live Demo: Instructor Dashboard
**Liuyi (0:25)**: 
> "For instructors, we built an analytics dashboard. We created a mock data seeding script to populate the database with realistic student data and generated quiz submissions. This allows instructors to instantly view actionable metrics, such as the overall class average and detailed performance reports."

### 🔴 7. Live Demo: Student Experience
**Liuyi (0:30)**: 
> "Let's look at the student experience. After logging in, students are redirected to their enrolled modules via role-based routing. They can interact with the 3D flashcards generated by Jing's backend Agents and take interactive quizzes. Upon submitting a quiz, the system immediately provides LLM-driven feedback with animated UI elements, explaining the correct answers."

### 🔴 8. Playwright E2E Testing
**Liuyi (0:20)**: 
> "In addition to backend unit tests, we wanted to ensure a stable user journey. I configured Playwright to run automated end-to-end browser tests. These scripts simulate real user interactions—logging in, navigating to modules, and completing tasks—verifying that the entire system works properly."

### 🔴 9. CI/CD Pipeline & Security Gates
**Jing (0:40)**: 
> "To maintain production-level quality, we implemented a strict 9-stage CI/CD pipeline using GitHub Actions. I specifically configured multiple security gates, including Gitleaks for detecting secrets, npm audit for frontend vulnerability scanning, and Bandit for Python static analysis. Our code is continuously linted, type-checked, and tested before merging and deployment."

### 🔴 10. Claude Code Mastery
**Jing (0:40)**: 
> "We fully integrated the extensibility of Claude Code into our team workflow. For instance, we configured custom Skills to accelerate routine tasks and set up a PreToolUse Stop hook that automatically intercepts any git commit if the test suite fails. We also connected a GitHub MCP server, allowing the Agent to read issues directly. Furthermore, we utilized an AI Code Reviewer Agent to autonomously evaluate our Pull Requests using the C.L.E.A.R. framework prior to merging."

### 🔴 11. Conclusion
**Liuyi (0:15)**: 
> "In summary, LearnMateAI demonstrates how advanced AI tools like Claude Code can accelerate development while maintaining enterprise-grade quality and testing standards."

**Jing (0:10)**: 
> "Thank you for watching our presentation."

---

## 📊 Presentation Overview

- **Duration**: 5-10 minute video demonstration
- **Content**: Showcase the application and Claude Code workflow
- **Slide Count**: 11 pages (estimated presentation time 7-8 minutes)
