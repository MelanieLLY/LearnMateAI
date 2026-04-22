
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

  - [Placeholder: Mermaid architecture diagram from `README.md`]
  - [Placeholder: Tech stack icons compilation]

### 4. Backend AI Agents & TDD

  - Test-Driven Development (TDD) workflow demonstration (Failing RED tests -> Passing GREEN tests).
  - Agent SDK code implementation.

  - ![Terminal TDD Test Screenshot](docs/screenshot/01_RED_phase_failing_tests.png)
  - ![Agent SDK Code Snippet](https://github.com/user-attachments/assets/e6a8983e-13e3-437e-a25f-5233e896c3b6)

### 5. Frontend UI & Parallel Development

  - Parallel development of UI components using `git worktree`.
  - Interactive quiz and 3D flashcards.

  - ![Parallel Git Worktree Terminals](docs/screenshot/17_evidence_7b_parallel_terminals.png)
  - [Placeholder: Interactive Quiz and 3D Flashcard UI Mockup]

### 6. Live Demo: Student Experience

  - Student Login -> Browse Modules -> Flip 3D Flashcards -> Complete Quiz & AI Feedback.

  - ![Student UI Experience](docs/screenshot/23_student_ui_experience.gif)

### 7. Live Demo: Instructor Dashboard

  - Instructor Login -> View Class Average and Module Trends.

  - ![Instructor Dashboard](docs/screenshot/21_instructor_dashboard.gif)

### 8. Playwright E2E Testing

  - Automated end-to-end browser test run results.

  - ![Playwright E2E Test All Green](docs/screenshot/18_evidence_11_playwright_e2e_report.png)

### 9. CI/CD Pipeline & Security Gates

  - 9-stage GitHub Actions workflow.
  - Security Checks: Gitleaks, npm audit, Bandit.

  - ![GitHub Actions Workflow All Green](docs/screenshot/19_evidence_9_github_actions_all_green.png)
  - ![GitHub PR Checks All Green](docs/screenshot/22_evidence_12_github_actions_pr.gif)

### 10. Claude Code Mastery

  - PreToolUse Stop hook (blocking unqualified commits).
  - GitHub MCP server connection.
  - AI Code Reviewer Agent based on the C.L.E.A.R. framework.

  - ![Stop Hook Blocking Commit](docs/screenshot/13_evidence_2_stop_hook.png)
  - ![AI Code Review PR Screenshot](docs/screenshot/20_evidence_10_clear_pr_comment.png)

### 11. Conclusion & Q&A

  - Core Highlights: Production Ready, Robust AI Workflow, Automated Security.
  - Q&A Session.

  - [Placeholder: Q&A Ending Background Image]

---
<br><br><br><br><br><br><br><br><br><br>
*(Scroll down to view speaker scripts)*
---

## 🎙️ Scripts / 演讲台词 (中英对照讲解用)

### 🔴 1. 介绍
**Jing (0:15)**: 
> "大家好，欢迎来到我们的 Project 3 演示。很高兴向大家介绍 LearnMateAI，这是一款使用 Claude Code 构建的生产级教育应用。我是 Jing，主要负责后端架构、生成式 AI Agent 集成、CI/CD 安全管道以及测试驱动开发 (TDD)。"

**Liuyi (0:15)**: 
> "我是 Liuyi。我负责前端 UI 和交互设计、Playwright 端到端测试、Render 和 Vercel 的 CI/CD 部署逻辑，以及配置 Hooks 和 MCP 等 Claude Code 核心工具。"

### 🔴 2. 项目概述与问题
**Liuyi (0:30)**: 
> "LearnMateAI 解决了自动化、互动式学习资源匮乏的问题。我们的平台允许讲师即时生成 3D 抽认卡和测验等学习材料，同时实时跟踪学生的表现。该应用已完全部署，大家现在就可以通过我们的公开 URL 访问。"

### 🔴 3. 系统架构
**Liuyi (0:25)**: 
> "我们的系统架构严格分离了前端和后端。客户端界面使用 React 和 Vite，与 Python FastAPI 后端进行通信。我们的数据存储在托管于 Render 的 PostgreSQL 中，前端则通过 Vercel 部署。"

### 🔴 4. 后端 AI 代理与 TDD
**Jing (0:45)**: 
> "在核心后端服务方面，我们严格遵循了测试驱动开发 (TDD) 的工作流程。正如 Git 历史记录所示，我总是先编写失败的单元测试并提交，然后再实现 API 以通过这些测试。为了满足生成式 AI 的需求，我构建了 3 个独立的 Agent SDK 功能来生成课程总结、抽认卡和测验。这确保了生成内容的可靠性，并且在我们的 96 个 Pytest 测试用例中得到了充分的测试。"

### 🔴 5. 前端 UI 与并行开发
**Liuyi (0:30)**: 
> "在后端开发的同时，我们利用 Git Worktrees 在同一个仓库中进行并行开发。我运行了多个终端会话，在一个 worktree 中构建交互式测验 UI，在另一个 worktree 中构建 3D 抽认卡 UI。这彻底隔离了我们的工作，使我们能够在没有 Git 冲突的情况下快速迭代 UI。"

### 🔴 6. 现场演示：学生体验
**Liuyi (0:30)**: 
> "让我们来看看学生的体验。学生登录后，系统会通过基于角色的路由将他们顺利重定向到已注册的模块。他们可以与 Jing 的后端 Agent 生成的 3D 抽认卡进行交互，并参与互动式测验。提交测验后，系统会立即提供带有动画效果的 LLM 驱动反馈，解释正确答案。"

### 🔴 7. 现场演示：讲师仪表板
**Liuyi (0:25)**: 
> "针对讲师，我们构建了一个分析仪表板。我们创建了一个模拟数据填充脚本，将逼真的学生数据和生成的测验提交记录填充到数据库中。这使讲师能够立即看到可操作的指标，例如班级整体平均分和详细的成绩报告。"

### 🔴 8. Playwright 端到端测试
**Liuyi (0:20)**: 
> "除了后端单元测试，我们还希望保证稳定的用户旅程。我配置了 Playwright 来运行自动化的端到端浏览器测试。这些脚本模拟了真实用户的交互——登录、导航到模块并完成任务——确保整个系统完美运行。"

### 🔴 9. CI/CD 管道与安全门控
**Jing (0:40)**: 
> "为了保持生产环境的质量，我们使用 GitHub Actions 实施了严格的 9 阶段 CI/CD 管道。我重点配置了多个安全门控，包括用于检测密钥的 Gitleaks、用于前端漏洞扫描的 npm audit 以及用于 Python 静态分析的 Bandit。我们的代码在合并和部署之前会不断进行代码检查 (linting)、类型检查和测试。"

### 🔴 10. Claude Code 高级应用
**Jing (0:40)**: 
> "我们将 Claude Code 的扩展性完全整合到了我们的团队工作流中。例如，我们设置了一个 PreToolUse Stop hook，如果测试套件失败，它会自动拦截任何 git commit。我们还连接了 GitHub MCP 服务器，允许 Agent 直接读取 issues。此外，我们利用了一个 AI 代码审查 Agent，在合并前使用 C.L.E.A.R. 框架自动评估我们的 Pull Requests。"

### 🔴 11. 总结与问答
**Liuyi (0:15)**: 
> "总而言之，LearnMateAI 成功展示了如何使用 Claude Code 等高级 AI 工具在加速开发的同时，保持企业级的质量和测试标准。"

**Jing (0:10)**: 
> "感谢大家聆听我们的演示。我们很乐意回答大家的任何问题。"

---

## 📊 Presentation Overview

- **Duration**: 5-10 minute video demonstration
- **Content**: Showcase the application and Claude Code workflow
- **Slide Count**: 11 pages (estimated presentation time 7-8 minutes)
