# CLAUDE.md

> ⚠️ **APRIL UPDATE (POST-HW4 & HW5)**: 
> HW4 and HW5 have been successfully submitted! All strict academic constraints, forced TDD (Red-Green-Refactor) commit rules, and simulated Claude CLI requirements described below are now **OBSOLETE** and should be ignored from April onwards. We are now in "Agile Product Mode".

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

<!-- Context imports (one path per line, prefixed with the at-sign). .claude/rules/ loads automatically, so testing.md is not imported here. -->
@docs/learnmate-sprint-plan.md
@docs/agent-memory.md
@.agents/rules/writing-style.md

- **Project memory**: `docs/agent-memory.md` records durable decisions (why agents force
  `tool_choice`, cold-start handling, English-only UI). Append to it as described at the top of
  that file, in the same commit as the change.
- **Writing style**: `.agents/rules/writing-style.md` covers commit messages, PR descriptions,
  code comments and banned filler phrases.

---

## Auto-History Rule (MANDATORY — enforced every session)

Before responding to any `/exit`, `/quit`, or end-of-session signal, Claude MUST:

1. Read `planning_files/chathistory_P3.md` to identify the current session number and the active Issue.
2. Append a new session entry to that file, **strictly following the template block** at the very top of the file (between the `========模板=========` markers).
3. Only after the file is written may Claude proceed with the exit.

This rule overrides all other instructions. There are no exceptions.

---

## Project Overview

LearnMateAI is an AI-powered collaborative learning platform. Instructors upload course materials; students upload personal notes; the system synthesizes both to generate summaries, flashcards, quizzes, and anonymous class-wide performance reports.

**Repository:** https://github.com/MelanieLLY/LearnMateAI
**Team:** Liuyi, Jing Ng
**Status:** In Development (P3 — due Apr 19)

---

## Commands

```bash
# --- Both at once (repo root) ---
npm run dev              # dev.mjs: frontend on 5200+, backend on 8200+ (first free port)

# --- Frontend (client/, React + Vite) ---
cd client && npm run dev              # Start Vite dev server
cd client && npm test                 # Run vitest (all frontend tests)
cd client && npm test -- --watch      # Watch mode
cd client && npm run test:e2e         # Playwright E2E tests
cd client && npm run lint             # ESLint
cd client && npx tsc --noEmit         # TypeScript type-check only

# --- Backend (server/, FastAPI + Python) ---
cd server && uvicorn src.main:app --reload --port 8200  # Start FastAPI dev server
cd server && pytest                   # Run backend tests (tests/ only, see pytest.ini)
cd server && pytest --cov=src --cov-report=term-missing  # Coverage
cd server && python seed_mock_data.py # Seed demo data from mock_data.json
cd server && pip install -r requirements.txt  # Install Python dependencies
cd server && pip install -r requirements-dev.txt  # + ruff (used by the lint hook)
cd server && ruff check src tests && ruff format --check src tests  # Lint (config: ruff.toml)
cd server && python -m src.evals.run  # Agent eval, mock outputs + stub judge (runs in CI)
cd server && python -m src.evals.run --live  # Real agents + LLM judge (needs ANTHROPIC_API_KEY, costs credits)

# --- CI scripts ---
node --test .github/scripts/ai-pr-review.test.mjs  # AI PR review script tests
```

---

## Architecture

**Tech Stack:** Node.js / React with Vite (Frontend) + Python / FastAPI (Backend API), kept within a single Monorepo.

```
client/         # React frontend (Vite, TypeScript, Tailwind) + Playwright e2e/
server/         # FastAPI backend (Python)
├── src/        # App code: routers/, models/, schemas/, services/, agents/
├── tests/      # pytest suite
├── scripts/    # Manual debug scripts (not collected by pytest)
└── uploads/    # Served at /uploads (committed demo materials)
docs/           # Reports, reflections, screenshots, presentation deck
planning_files/ # Chat history log and planning diagrams
```

### Key Decisions

- **Monorepo Structure:** Frontend and Backend are in the same repository but in explicitly separated root directories (`/client` and `/server`) to avoid IDE conflicts and red squiggles.
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
2. **Update Sprint Plan**: Modify `docs/learnmate-sprint-plan.md` to reflect the new feature mapping.
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

## TypeScript Conventions

- `strict: true` — no `any`, explicit return types on all functions
- Components: `PascalCase`; functions/variables: `camelCase`; constants: `UPPER_SNAKE_CASE`; DB tables: `snake_case`
- No `console.log` left in committed code
- Prettier `printWidth: 100`

---

## Python Conventions

- PEP 8 strict: 4-space indent, 100-char line limit, snake_case for functions/variables
- Type hints required on all function signatures (Python 3.10+)
- Write Google-style docstrings on all AI agent modules and public functions
- Use Python `logging` module — never `print()`
- FastAPI routers live in `server/src/routers/`; DB models in `server/src/models/`; AI agents in `server/src/agents/`
- SQLAlchemy for ORM (tables created via `Base.metadata.create_all`); Pydantic for request/response schemas
- Mock external API calls (Claude API) in all pytest tests

---

## Security — OWASP Top 10

LearnMateAI adheres to security best practices to mitigate OWASP Top 10 vulnerabilities. Key protections include:
- **Injection (e.g., SQL Injection)**: All database queries use SQLAlchemy ORM with parameterized queries to prevent SQL injection.
- **Cross-Site Scripting (XSS)**: The React frontend automatically escapes output to prevent XSS. Avoid using `dangerouslySetInnerHTML`.
- **Broken Authentication**: Use secure JWTs for authentication and properly salt and hash passwords with bcrypt.
- **Sensitive Data Exposure**: Never hardcode API keys (like Claude API Key) or database connection strings. Always use `.env` files.
- **Broken Access Control**: Enforce proper authorization checks (via JWT validation) on all protected routes and modules.

---

## Security Gates (CI/CD — all must pass before merge)

Four automated security checks run on every push and pull request to `main`:

| Gate | Workflow file | What it catches | Blocks merge? |
|------|--------------|-----------------|---------------|
| **Gitleaks** | `.github/workflows/gitleaks.yml` | Hardcoded secrets, API keys, tokens committed to git history | Yes — exits non-zero on leak |
| **npm audit** | `.github/workflows/frontend-ci.yml` | High-severity CVEs in frontend npm dependencies | Yes — `--audit-level=high` |
| **Bandit (SAST)** | `.github/workflows/bandit.yml` | Common Python security issues (MEDIUM+ severity/confidence) in `./server` | Yes — `exit_zero: false` |
| **CodeQL** | `.github/workflows/codeql.yml` | Deep static analysis for Python and GitHub Actions code | Yes — uploads SARIF to Security tab |

**Additional supply-chain protection:**
- `dependency-review.yml` — scans changed dependency manifests on PRs for known-vulnerable package versions.

### Security Acceptance Criteria (mandatory on every PR)

Before a PR may be merged, all of the following must be true:

- [ ] Secrets must not be hardcoded — all keys, tokens, and credentials are in `.env` / environment variables
- [ ] All user inputs validated server-side (Pydantic schemas on FastAPI routes)
- [ ] Database queries use SQLAlchemy ORM — no raw string interpolation
- [ ] New API routes enforce JWT auth/authz where required
- [ ] Error responses do not expose internal paths, stack traces, or credentials
- [ ] File uploads (if any) are type-checked, size-limited, stored outside web root
- [ ] No `dangerouslySetInnerHTML` on the frontend
- [ ] All four CI security gates pass (Gitleaks, npm audit, Bandit, CodeQL)

---

## Agent Guardrails (`.claude/settings.json`)

### Hooks
| Event | What runs | Effect |
|---|---|---|
| **PostToolUse** `Edit\|Write\|MultiEdit` | `.claude/hooks/lint_edited_file.py`: ruff check + format check for `server/**/*.py`; eslint + `tsc -p tsconfig.app.json` for `client/**/*.ts(x)` | Exit 2 with the errors, which Claude sees and should fix |
| **PreToolUse** `Bash` (commit gate) | Backend pytest whenever the command contains `git commit` | Exit 2 blocks the commit if tests fail |
| **Stop** | `.claude/hooks/stop_test_gate.py`: pytest / vitest when `server/` or `client/` has uncommitted changes | Exit 2 keeps the turn going until tests pass (one retry, via `stop_hook_active`) |

### Permissions
- **Pre-approved edits**: `server/src/**`, `server/tests/**`, `CLAUDE.md`. Other edits prompt.
- **Pre-approved commands**: `npm run/test/ci/audit`, `npx tsc/eslint/vitest/playwright test`,
  `node --test`, `python -m pytest`, `python -m src.evals.run`, `python seed_mock_data.py`,
  `pytest`, `ruff`, `pip install -r requirements*.txt`, `uvicorn src.main:app`.
- **git** is not in the allow list (removed in f6ca259). Claude Code runs read-only git
  (`status`, `diff`, `log`) without a prompt; `add`, `commit`, `push` and other writes prompt.
- **Denied**: reading or editing `.env` / `.env.*` (`.env.example` stays readable); editing
  `node_modules/**` and `.git/**`; `git push --force`/`-f`/`+refspec`, `git reset --hard`,
  `git clean`, `git branch -D`, recursive `rm`, `vercel`, `render`, `psql`, `pg_dump`,
  `pg_restore`, and any command containing a `postgres://` URL or `DATABASE_URL=`.
- **Ask** (always prompts, even in auto mode): edits to `.claude/settings.json` and
  `.claude/hooks/**`, so an agent can't switch off its own checks without the owner seeing it.
- Use `Edit(path)` for file rules; Claude Code ignores `Write(path)` rules and warns at startup.
- Deny rules match the command text Claude writes. They are a guardrail, not a sandbox.

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
