# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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

**Monolith MVP:** Single Next.js (App Router) + Express codebase.

```
src/
├── app/            # Next.js App Router pages and API routes
├── features/
│   ├── instructor/ # uploadMaterial, getAnalytics
│   ├── student/    # submitNotes, takeQuiz, getHint
│   ├── synthesis/  # generateSummary, generateFlashcards, generateQuiz (all call Claude API)
│   └── evaluation/ # evaluateContent (LLM-as-judge), calculateMetrics
├── api/            # Express route handlers (instructor, student, evaluation, auth)
├── services/
│   ├── claudeAPI.ts  # Single wrapper for all Claude API calls
│   ├── storage.ts    # File system (dev) / S3 (prod)
│   └── auth.ts       # JWT generation/verification
├── db/
│   └── client.ts   # Prisma client singleton
└── utils/          # logger, errors, constants
prisma/
├── schema.prisma   # Source of truth for all DB types
└── seed.ts
tests/
├── integration/    # Full user-flow tests (notes → quiz → feedback)
└── e2e/            # Playwright (instructor upload → generate → analytics)
```

### Key Decisions

- **Claude API for all AI:** synthesis, quiz generation, hints, and LLM-as-judge evaluation all go through `src/services/claudeAPI.ts`.
- **Prisma:** All DB access via Prisma ORM. SQLite in dev, PostgreSQL in prod — switching is transparent.
- **Authentication:** JWT with bcrypt. No OAuth for MVP.
- **File storage:** `./uploads/` in dev, AWS S3 in prod.
- **REST API endpoints:**
  - `POST /api/instructor/materials`, `GET /api/instructor/analytics`
  - `POST /api/student/notes`, `POST /api/student/quiz/:id/submit`
  - `POST /api/evaluation/assess`

---

## TDD Workflow (Required)

Every feature follows **Red → Green → Refactor**, each as a separate commit:

```bash
git commit -m "test(scope): RED - describe what fails"
git commit -m "feat(scope): GREEN - minimal implementation"
git commit -m "refactor(scope): improve quality"
```

Mock Claude API and DB calls in unit tests (`jest.mock()`). Integration tests under `tests/integration/` hit a real (test) database.

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
