# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

<!-- HW4 Required Context Imports -->
@import project_proposal.md
@import "planning files/learnmate-sprint-plan.md"

---

## Project Overview

LearnMateAI is an AI-powered collaborative learning platform. Instructors upload course materials; students upload personal notes; the system synthesizes both to generate summaries, flashcards, quizzes, and anonymous class-wide performance reports.

**Repository:** https://github.com/MelanieLLY/LearnMateAI
**Team:** Liuyi, Jing Ng
**Status:** In Development (P3 — due Apr 19)

---

## Commands

```bash
# --- Frontend (React + Vite, http://localhost:5173) ---
npm run dev              # Start Vite dev server
npm test                 # Run vitest (all frontend tests)
npm test -- --watch      # Watch mode during TDD
npm test -- generateQuiz.test.ts  # Single test file
npm test -- --coverage   # Coverage report
npm run test:e2e         # E2E tests
npm run lint             # ESLint
npx tsc --noEmit         # TypeScript type-check only

# --- Backend (FastAPI + Python) ---
uvicorn src.backend.main:app --reload  # Start FastAPI dev server (http://localhost:8000)
pytest                   # Run all backend tests
pytest tests/backend/    # Run backend tests only
pytest --cov=src/backend --cov-report=term-missing  # Coverage
alembic upgrade head     # Run DB migrations
alembic revision --autogenerate -m "<migration_name>"  # Generate migration
pip install -r requirements.txt  # Install Python dependencies
```

---

## Architecture

**Tech Stack:** Node.js / React with Vite (Frontend) + Python / FastAPI (Backend API), kept within a single Monorepo.

```
src/
├── frontend/       # React Frontend (Vite, TypeScript, Tailwind)
└── backend/        # FastAPI Backend (Python)
    └── db/         # PostgreSQL Database schemas and ORM clients
```

### Key Decisions

- **Monorepo Structure:** Frontend and Backend are in the same repository but in explicitly separated subdirectories (`/frontend` and `/backend`) to avoid IDE conflicts and red squiggles.
- **LLM Engine:** All Claude API calls handled by dedicated AI agent modules in the Python backend.
- **Testing:** We use `vitest` for frontend testing and `pytest` for backend testing (minimum 80% coverage).
- **Authentication:** JWT with bcrypt. No OAuth for MVP.

---

## TDD Workflow (Required)

Every feature follows **Red → Green → Refactor**, each as a separate commit:

```bash
git commit -m "test(scope): RED - describe what fails"
git commit -m "feat(scope): GREEN - minimal implementation"
git commit -m "refactor(scope): improve quality"
```

Tests MUST be written BEFORE implementation code. Mock external API calls.

---

## Do's and Don'ts (Strictly Enforced)

### Feature Development Workflow (ALWAYS DO THIS)
Whenever you start adding or modifying a feature, you MUST process the following:
1. **GitHub Issue**: Create or update the relevant GitHub Issue, adding appropriate labels and milestones.
2. **Update Sprint Plan**: Modify `planning files/learnmate-sprint-plan.md` to reflect the new feature mapping.
3. **Branching**: Checkout a new Git branch utilizing the issue ID (e.g., `feat/42-description` or `fix/15-bug`).

### Do's
- Write failing tests first.
- Strict adherence to PEP 8 for Python and Strict Mode for TypeScript.
- Write high-quality docstrings for Python AI algorithms.
- Commit frequently with conventional commits containing Issue IDs (e.g., `feat(#2): add module API`).

### Don'ts
- **No `any` types** in TypeScript.
- **Never mask TS errors** with `// @ts-ignore`.
- **Never hardcode secrets** (Claude API keys, DB strings) in public files; use `.env`.
- Do not modify frontend routes when assigned a backend task unless specifically requested.

---

---

## TypeScript Conventions

- `strict: true` — no `any`, explicit return types on all functions
- Components: `PascalCase`; functions/variables: `camelCase`; constants: `UPPER_SNAKE_CASE`; DB tables: `snake_case`
- Use `logger` utility (from `src/frontend/utils/logger.ts`), never `console.log`
- Prettier `printWidth: 100`

---

## Python Conventions

- PEP 8 strict: 4-space indent, 100-char line limit, snake_case for functions/variables
- Type hints required on all function signatures (Python 3.10+)
- Write Google-style docstrings on all AI agent modules and public functions
- Use Python `logging` module — never `print()`
- FastAPI routers live in `src/backend/routers/`; DB models in `src/backend/models/`; AI agents in `src/backend/agents/`
- SQLAlchemy for ORM; Alembic for migrations; Pydantic for request/response schemas
- Mock external API calls (Claude API) in all pytest tests

---

## Permissions (`.claude/settings.json`)

Write access is scoped to `src/**`, `tests/**`, `CLAUDE.md`.
Disallowed: `.env`, `node_modules/**`, `.git/**`.
Allowed commands: `npm`, `git`, `npx`, `node`, `python`, `python3`, `pytest`, `pip`, `pip3`, `uvicorn`, `alembic`.

## Context Management

Claude Code has a 1M token context window. Manage it strategically:

### /clear
Clear conversation history when:
- Switching to a completely different feature
- Context usage exceeds 70%
- After /compact to actually reset
```bash
/clear
# Then explain what you're working on next
```

### /compact
Summarize conversation to save tokens when:
- Context exceeds 60% (Claude Code will suggest it)
- Between major phases (Explore → Plan → Implement)
- After long debugging sessions
```bash
/compact
# Claude creates a summary, frees up tokens
```

### --continue
Resume previous session when:
- Working on same feature across multiple days
- Maintaining context for multi-part features
```bash
claude --continue
# Resumes last session with full context
```

### Smart Context Distribution

**In CLAUDE.md (Persistent):**
- Architecture decisions
- Coding conventions
- Tech stack details
- Available commands
- Testing strategy

**In Conversation (Session):**
- Current feature details
- Test cases
- Implementation decisions
- Error messages

**Between Sessions (Git):**
- Code commits
- Tests
- Database schema
