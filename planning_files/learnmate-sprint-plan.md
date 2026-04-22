# LearnMateAI Sprint Plan

> 2 sprints · 2 developers · ~2 weeks each
> Deadline: Apr 19

> **the required Retrospectives are at the end of this document**

---

## Sprint 1: Foundation + Module System (Mar 24 – Mar 30)

**Day 1-2: Person A solo — Sprint 1: System Foundation & Scaffolding**
- Next.js + FastAPI project setup, folder structure, DB schema
- Auth system: JWT login/register, role-based middleware (student / instructor / admin) [#17]
- GitHub org + repos, CI/CD pipeline (GitHub Actions: lint + test on PR)
- CLAUDE.md configured (including project context, stack, testing strategy, and permissions setup for HW4)
- Team contract established

**Day 3-7: Both devs in parallel**

| Person A | Person B |
|---|---|
| **Instructor Module Management Core API (Backend) (Target for HW4)**<br>**Instructor Module Management UI (Frontend)** | **Feature: Student module experience** |
| Module Management API (Create/Edit/Delete) | Student module list + browse UI [#16] |
| Instructor UI for Module Management [#15] | View/download materials page [#16] |
| Upload materials to S3 (API + UI) [#15] | Student note upload (API + UI) [#16] |
| Define learning objectives per module | |

> ~~**🤖 CLAUDE CODE PROMPT FOR HW4 (Module Management API)**~~
> *(✅ STATUS: HW4 SUBMITTED. The strict Claude Code CLI TDD workflow and formatting constraints below are no longer enforced. We are free to refactor and develop normally.)*
> ~~Claude, build the "Module Management API" backend feature using strict TDD. Follow this exact 4-phase workflow (Explore → Plan → Implement → Commit):~~
> ~~1. **Explore:** Use Glob, Grep, Read to understand the existing code stack and directory structure.~~
> ~~2. **Plan:** Use Plan mode to outline the backend endpoints. Write failing tests first.~~
> ~~3. **Implement (TDD):** Run tests (Red), implement minimum code to pass (Green), and refactor. Repeat for all API operations.~~
> ~~4. **Commit:** Create clean commits with meaningful messages showing the Red-Green-Refactor process for git history.~~

**Sprint 1 deliverables:**
- Auth flow end-to-end
- Instructor Module APIs (Developed strictly via TDD for HW4)
- Student browses modules, views materials, uploads personal notes
- CI/CD: auto test + deploy to dev on merge
- CLAUDE.md + team contract
- **Async Standups**: 3 sessions completed per partner in this sprint (Slack/Discord logged).
- ~~**HW4 Target:** Annotated Claude Code session log~~ (✅ Submitted)
- ~~**HW4 Target:** 1-2 page reflection document on workflow~~ (✅ Submitted)

---

## Sprint 2: AI Core Features, Reports & Deployment (Mar 31 – Apr 15)

| Person A | Person B |
|---|---|
| **Feature: Agentic Content Generation (Backend)** | **Parallel Development (Frontend)** |
| Context builder: merge materials + notes (Completed) | **Feature A (Issue #24)**: Quiz-taking UI (Completed) |
| Feature 1: Study Summary Generation Agent (Completed) | **Feature B (Issue #33)**: Flashcards & Summary UI (Completed) |
| Feature 2: Flashcard Gen Agent (Completed) | |
| Feature 3: Quiz Gen Agent & API (Completed) | |
| Quiz submission API + answer storage (Completed) | |
| Bugfix (Issue #38): Migrate AI agents to use tool structured outputs (Completed) | **Feature (Issue #42)**: Student enrollment system & auth hardening (Completed) |
| Bugfix (Issue #40): Fix stringified tool output parsing and refine AI prompts (Completed) | **Feature (Issue #43)**: Simulate mock data to prepare for testing (Completed) |
| Eval system for outputs | **Test (Issue #21)**: Set up Playwright for E2E tests (Completed) |
| Store eval history in DB for reporting | **Feature (Issue #49)**: Improve mock data realism |
| | **Feature (Issue #51)**: UX Improvements (Login Auto-Routing & Group Modules) (Completed) |

**Sprint 2 deliverables:**
- 3+ distinct features built with parallel agents (Summary, Flashcard, Quiz)
- chore: Setup everything-claude-code ecosystem, playbooks, and automated hooks
- chore (Issue #34): Set up frontend testing framework (Vitest & Playwright)
- Summary, flashcards, quiz all render correctly
- Student takes quiz, gets pre-generated hints for MCQ and dynamic hints for open-ended
- Eval engine auto-scores every LLM generation using LLM-as-judge, history stored
- CI/CD: add staging environment

**(Sprint 2 Part 2: Reports & Polish)**

| Person A | Person B |
|---|---|
| **Feature (Issue #6): Instructor report** | **Feature: System Eval & MLOps** |
| Aggregated class report API (anonymous stats) (Completed) | Eval metrics dashboard (For dev/testing view) |
| Report dashboard UI (common gaps, avg scores) (Completed) | LLM quality trend charts & LLM-as-judge reports |
| | |
| **Feature: Production & Polish** | |
| Feature (Issue #58): Cloud Database Fallback & psycopg2 (Completed) | CI/CD Deploy configuration for Render / Vercel (Completed) |
| Sentry + Grafana setup | UI polish (loading states, responsive) |
| Security (rate limiting, OWASP, secrets) | Documentation (README, API docs, blog post) |
| CI/CD: canary/blue-green deploy to prod | Presentation slides |

**Sprint 2 Overall Polish deliverables:**
- Instructor anonymous class performance report
- Eval trend graphs & generation metrics dashboard for testing
- Sentry + Grafana dashboards live
- Security hardened, production deployed
- Documentation package complete
- **Async Standups**: 3 sessions completed per partner in this sprint (Slack/Discord logged).
- PR code reviews all correctly tagged with C.L.E.A.R. framework.

---

## Apr 16 – Apr 19: Buffer

- Rehearse 20-min presentation
- Individual reflections + peer evaluations
- Bug fixes only, no new features
- Bugfix (Issue #53): Fix student flashcard generation model and Load Existing student filtering (Completed)
- Bugfix (Issue #56): Implement split-screen UI layout for course/module browsing (Completed)
- Refactor (Issue #64): Translate all UI and seed data to English (Completed)
- Docs (Issue #65): README (Completed)
- Bugfix (Issue #69): Fix Module creation not binding to course

---

## Sprint 1 Retrospective (Mar 24 – Mar 30)
**What went well:** 
* Successfully laid down the Next.js and FastAPI foundations, establishing early CI/CD integration and deployment workflows.
* Auth system (JWT roles) worked cleanly preventing access crossovers.
* Nailed the strict Test-Driven Development (TDD) workflow required for HW4. We merged quality, thoroughly-tested code for the Instructor Module Management API.
* Good collaboration and visibility maintained through regular async standups.

**What could be improved:**
* Dealing with strict TDD and Claude CLI constraints slowed down rapid prototyping initially, though it ensured better stability long-term.

**Action Items:**
* Transition away from strict HW4 constraints and pivot hard towards complex parallel AI Agent generation tasks for Sprint 2.

---

## Sprint 2 Retrospective (Mar 31 – Apr 15)
**What went well:**
* Immense engineering progress on Agentic content (Flashcards, Quizzes, Summaries).
* Effectively resolved difficult AI integration bugs, specifically migrating agents to structured tool outputs and fixing stringified JSON parsing (Issues #38 & #40).
* Frontend team delivered outstanding UX (Stepper quiz UI, 3D flashcards, split-screen module browsing).
* MLOps/Eval pipelines and Instructor analytics architectures were successfully put in place.

**What could be improved:**
* Managing mock data versus real data flow, and handling database fallbacks (psycopg2) created unexpected overhead.
* LLM hallucinations during early testing required multiple prompt refinement iterations.

**Action Items:**
* Enter code freeze for new features. Focus entirely on bug fixes (e.g., UI translation, filter refinements), project presentations, and documentation polish before the final deadline.
