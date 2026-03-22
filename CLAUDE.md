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
# Dev server (Next.js, http://localhost:3000)
npm run dev

# All tests
npm test

# Tests in watch mode (use during TDD)
npm test -- --watch

# Single test file
npm test -- generateQuiz.test.ts

# Coverage
npm test -- --coverage

# E2E tests
npm run test:e2e

# Lint
npm run lint

# Type check only
npx tsc --noEmit

# Prisma migrations
npx prisma migrate dev --name <migration_name>
npx prisma studio        # Visual DB browser
npx prisma db seed
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
- Use `logger` utility (from `src/utils/logger.ts`), never `console.log`
- Prettier `printWidth: 100`

---

## Permissions (`.claude/settings.json`)

Write access is scoped to `src/**`, `tests/**`, `prisma/**`, `CLAUDE.md`.
Disallowed: `.env`, `node_modules/**`, `.git/**`.
Allowed commands: `npm`, `git`, `npx`, `node`.

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
