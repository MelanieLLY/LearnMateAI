# HW4 Work Summary: Claude Code Workflow & TDD
**LearnMateAI — CS7180 Project 3 | Part 4: Reflection**

---

## Table of Contents

1. [Project Setup](#1-project-setup)
2. [Work Completed: Three CRUD APIs](#2-work-completed-three-crud-apis)
3. [TDD Process](#3-tdd-process)
4. [Git History](#4-git-history)
5. [Test Results](#5-test-results)

---

## 1. Project Setup

### 1.1 CLAUDE.md Configuration

The `CLAUDE.md` file serves as the persistent project context document for Claude Code. It was authored collaboratively through the `/init` workflow and iteratively refined based on Claude's own suggestions.

**Key sections configured:**

| Section | Content |
|---|---|
| **Tech Stack** | React + Vite (TypeScript) frontend; FastAPI (Python) backend; SQLite (dev) / PostgreSQL (prod); pytest; vitest |
| **Architecture** | Monorepo with `/frontend` and `/server` split; LLM AI agents in `server/src/agents/`; JWT auth |
| **Commands** | Full command table for frontend (`npm run dev`, `npm test`) and backend (`uvicorn`, `pytest`, `alembic`) |
| **TypeScript Conventions** | `strict: true`, no `any`, PascalCase components, `UPPER_SNAKE_CASE` constants |
| **Python Conventions** | PEP 8, type hints on all signatures, Google-style docstrings, `logging` module, never `print()` |
| **Testing Strategy** | vitest (frontend) + pytest (backend); minimum 80% coverage; TDD mandatory |
| **Do's / Don'ts** | No hardcoded secrets, no `@ts-ignore`, no masking errors, mandatory Issue tracking before branching |
| **Security (OWASP Top 10)** | SQLAlchemy ORM for parameterized queries, HttpOnly cookie for JWT, bcrypt password hashing |
| **`@import` References** | Imports `planning_files/project3_proposal.md`, `planning_files/learnmate-sprint-plan.md`, and `.claude/rules/common/testing.md` |

**Initial `/init` output (key corrections Claude identified):**
```text
1. CLAUDE.md referenced "Next.js" but stack is Vite/React — corrected.
2. CLAUDE.md had Prisma commands but backend is Python/FastAPI — replaced with
   uvicorn, pytest, alembic, pip commands.
3. settings.json used non-standard format for permissions — rewritten to use
   proper Bash(cmd:*) allowlist patterns.
```

---

### 1.2 `.claude/settings.json` — Permissions Configuration

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "WriteFile",
        "hooks": [{ "type": "command", "command": "echo '[Claude Code] File saved. Remember to run linter! (HW grading hook)'" }]
      },
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "echo 'Please remember to run /chat-history-log before you exit!'" }]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": "INPUT=$(cat); if echo \"$INPUT\" | grep -q 'git commit'; then echo '🛑 [STOP HOOK] Tests must pass before commit! Run: cd server && pytest' >&2; exit 2; else exit 0; fi"
        }]
      }
    ]
  },
  "permissions": {
    "allow": [
      "Bash(npm:*)", "Bash(npx:*)", "Bash(node:*)",
      "Bash(python:*)", "Bash(python3:*)",
      "Bash(pytest:*)", "Bash(pip:*)", "Bash(pip3:*)",
      "Bash(uvicorn:*)", "Bash(alembic:*)",
      "Edit(server/src/**)", "Write(server/src/**)",
      "Edit(server/tests/**)", "Write(server/tests/**)",
      "Edit(CLAUDE.md)", "Write(CLAUDE.md)"
    ],
    "deny": [
      "Edit(.env)", "Write(.env)",
      "Edit(node_modules/**)", "Write(node_modules/**)",
      "Edit(.git/**)", "Write(.git/**)"
    ]
  }
}
```

**Notable hooks configured:**
- `PreToolUse` Bash hook: Intercepts any `git commit` command and **blocks it** (`exit 2` to `stderr`) until tests pass. This was debugged extensively — `exit 1` alone was insufficient; only `exit 2` physically blocks Claude Code.
- `PostToolUse` Bash hook: Reminds Claude to log the session before exiting.

---

### 1.3 Tech Stack Summary

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, TypeScript (`strict: true`), Tailwind CSS |
| Backend | Python 3.12, FastAPI, SQLAlchemy ORM, Alembic migrations, Pydantic schemas |
| Auth | JWT (python-jose), bcrypt password hashing, HttpOnly cookie |
| Database | SQLite (dev / in-memory for tests), PostgreSQL (prod) |
| Testing | pytest + pytest-cov (backend); vitest (frontend) |
| Storage | Local `/uploads/` folder with optional S3 upgrade via env var detection |

---

## 2. Work Completed: Three CRUD APIs

The selected P3 feature for HW4 was **Instructor Module Management API** (Issue #2), covering Create, Edit, and Delete operations on learning modules.

All three APIs are implemented in:
- `server/src/routers/modules.py` — thin FastAPI route handlers
- `server/src/services/module_service.py` — business logic (no DB code in routes)
- `server/src/schemas/module.py` — Pydantic request/response schemas

---

### 2.1 Create Module API (`POST /api/v1/modules`)

#### Red Phase — Failing Tests Written First

**File:** `server/tests/test_create_module.py`

| # | Scenario | Expected Status |
|---|---|---|
| 1 | Happy Path: valid payload + instructor token | 201 Created |
| 2 | Missing Title: payload without `title` | 422 Unprocessable Entity |
| 3 | Empty Title: `title: ""` | 422 Unprocessable Entity |
| 4 | Duplicate Title: same instructor, same title twice | 409 Conflict |
| 5 | Unauthenticated: no Authorization header | 401 Unauthorized |
| 6 | Wrong Role: valid token but `role='student'` | 403 Forbidden |

**RED output (terminal):**
```text
================================ short test summary info =================================
FAILED tests/backend/test_create_module.py::TestCreateModule::test_create_module_success
FAILED tests/backend/test_create_module.py::TestCreateModule::test_create_module_missing_title
FAILED tests/backend/test_create_module.py::TestCreateModule::test_create_module_empty_title
FAILED tests/backend/test_create_module.py::TestCreateModule::test_create_module_duplicate_title
FAILED tests/backend/test_create_module.py::TestCreateModule::test_create_module_unauthenticated
FAILED tests/backend/test_create_module.py::TestCreateModule::test_create_module_student_role_forbidden
=================================== 6 failed in 0.11s ====================================
```
> Screenshot: `docs/screenshot/01_RED_phase_failing_tests.png`

**Commit:** `test(#2): RED - add failing tests for create module API`

---

#### Green Phase — Minimum Implementation

Claude implemented:
1. `ModuleCreate` Pydantic schema with `title` (required, min_length=1) and optional fields
2. `POST /modules` route handler delegating to `module_service.create_module()`
3. `create_module()` service function: duplicate-title check → create → commit → return

**GREEN output (terminal):**
```text
collected 6 items
tests/backend/test_create_module.py ...... [100%]
========= 6 passed, 4 warnings in 0.07s =========
```
> Screenshot: `docs/screenshot/02_01_GREEN_phase_passed.png`

**Commit:** `feat(#2): GREEN - implement create module API to pass tests`

---

#### Refactor Phase — Code Quality

Improvements applied:
- Extracted `create_module()` and `get_module_by_title()` into `module_service.py` (DRY principle)
- Added Google-style docstrings to all functions and route handlers
- Pinned all backend dependencies in `requirements.txt` to latest stable LTS versions
- Verified all 6 tests still pass after refactor

**Commit:** `refactor(#2): improve create module API structure and update dependencies`

---

### 2.2 Edit Module API (`PUT /api/v1/modules/{module_id}`)

#### Red Phase — Failing Tests Written First

**File:** `server/tests/test_edit_module.py`

| # | Scenario | Expected Status |
|---|---|---|
| 1 | Happy Path: valid update payload + owning instructor | 200 OK, updated fields returned |
| 2 | Partial Update: only some fields sent — omitted fields unchanged | 200 OK |
| 3 | Not Found: `module_id` that does not exist | 404 with `"module"` in detail |
| 4 | Unauthenticated: no Authorization header | 401 Unauthorized |
| 5 | Wrong Role: valid token but `role='student'` | 403 Forbidden |
| 6 | Wrong Owner: different instructor tries to edit another's module | 403 Forbidden |

**RED output (terminal):**
```text
================================ short test summary info =================================
FAILED tests/backend/test_edit_module.py::TestEditModule::test_edit_module_success
FAILED tests/backend/test_edit_module.py::TestEditModule::test_edit_module_partial_update
FAILED tests/backend/test_edit_module.py::TestEditModule::test_edit_module_not_found
FAILED tests/backend/test_edit_module.py::TestEditModule::test_edit_module_unauthenticated
FAILED tests/backend/test_edit_module.py::TestEditModule::test_edit_module_student_role_forbidden
FAILED tests/backend/test_edit_module.py::TestEditModule::test_edit_module_wrong_instructor
=================================== 6 failed in 0.08s ====================================
```
> Screenshot: `docs/screenshot/04_Edit_RED_phase_failing_tests.png`

**Commit:** `test(#2): RED - add failing tests for edit module API`

---

#### Green Phase — Minimum Implementation

Claude implemented:
1. `ModuleUpdate` Pydantic schema using `model_dump(exclude_unset=True)` for partial updates
2. `PUT /modules/{module_id}` route handler
3. `update_module()` service: lookup by ID → 404 if missing → 403 if wrong owner → apply fields → commit

**GREEN output (terminal):**
```text
collected 6 items
tests/backend/test_edit_module.py ...... [100%]
======================================= 6 passed in 0.05s ========================================
```
> Screenshot: `docs/screenshot/05_Edit_GREEN_phase_passed.png`

**Commit:** `feat(#2): GREEN - implement edit module API to pass tests`

---

#### Refactor Phase — Code Quality

Key improvement: The inline DB lookup `db.query(Module).filter(Module.id == module_id).first()` was extracted into a reusable `get_module_by_id(db, module_id)` helper — which the upcoming Delete API could then reuse, eliminating duplication.

```text
Before:  update_module() contained inline DB query
After:   get_module_by_id(db, module_id) → Module | None
         (mirrors existing get_module_by_title() pattern — DRY)
         Delete Module (next) will reuse it without duplication
```

**Commit:** `refactor(#2): improve edit module API structure`

---

### 2.3 Delete Module API (`DELETE /api/v1/modules/{module_id}`)

#### Explore & Plan Phase (before Red)

Claude used `Glob`, `Grep`, and `Read` to review existing schemas and routes, then produced a TDD plan:

```text
RED   — 5 tests will fail with {"detail":"Method Not Allowed"} (route missing)

GREEN — minimum implementation:
  1. delete_module(db, module_id, instructor_id) in module_service.py:
     - Call get_module_by_id() → raise 404 if None
     - Check module.instructor_id != instructor_id → raise 403
     - db.delete(module) + db.commit()
  2. @router.delete("/modules/{module_id}", status_code=204)
     - No response_model (204 has no body)
     - Return None (FastAPI sends empty response automatically)

REFACTOR — add docstrings; confirm 404/403 guard sequence matches update_module
```

#### Red Phase — Failing Tests Written First

**File:** `server/tests/test_delete_module.py`

| # | Scenario | Expected Status |
|---|---|---|
| 1 | Happy Path: owner deletes module → 204; second delete confirms row is gone → 404 | 204 + 404 follow-up |
| 2 | Not Found: `module_id` 99999 | 404 with `"module"` in detail |
| 3 | Unauthenticated: no Authorization header | 401 Unauthorized |
| 4 | Wrong Role: valid token but `role='student'` | 403 Forbidden |
| 5 | Wrong Owner: Instructor 2 cannot delete Instructor 1's module | 403 Forbidden |

**RED output (terminal):**
```text
=========================================================================================== short test summary info ============================================================================================
FAILED tests/backend/test_delete_module.py::TestDeleteModule::test_delete_module_success - AssertionError: {"detail":"Method Not Allowed"}
FAILED tests/backend/test_delete_module.py::TestDeleteModule::test_delete_module_not_found - AssertionError: {"detail":"Method Not Allowed"}
FAILED tests/backend/test_delete_module.py::TestDeleteModule::test_delete_module_unauthenticated - AssertionError: {"detail":"Method Not Allowed"}
FAILED tests/backend/test_delete_module.py::TestDeleteModule::test_delete_module_student_role_forbidden - AssertionError: {"detail":"Method Not Allowed"}
FAILED tests/backend/test_delete_module.py::TestDeleteModule::test_delete_module_wrong_instructor - AssertionError: {"detail":"Method Not Allowed"}
============================================================================================== 5 failed in 0.08s ===============================================================================================
```
> Screenshot: `docs/screenshot/06_Delete_RED_phase_failing_tests.png`

**Commit:** `test(#2): RED - add failing tests for delete module API`

---

#### Green Phase — Minimum Implementation

Claude implemented:
1. `delete_module()` service function reusing `get_module_by_id()` (no duplication)
2. `DELETE /modules/{module_id}` route, returns `None` → FastAPI auto-sends 204 empty body

**GREEN output (terminal):**
```text
collected 5 items
tests/backend/test_delete_module.py ..... [100%]
============================================================================================== 5 passed in 0.04s ===============================================================================================
```
> Screenshot: `docs/screenshot/07_Delete_GREEN_phase_passed.png`

**Commit:** `feat(#2): GREEN - implement delete module API to pass tests`

---

#### Refactor Phase — Code Quality

Only `module_service.py` was modified:

```text
1. Function order restored to standard CRUD sequence:
   Before:  get_by_id → get_by_title → create → delete → update
   After:   get_by_id → get_by_title → create → update → delete
   (delete was inserted mid-file during GREEN; moved to end)

2. Returns section added to delete_module():
   Before:  only function in file without a Returns section
   After:   "Returns: None. The row is removed from the database..."
   (makes docstring style uniform across the entire module)
```

**Commit:** `refactor(#2): improve delete module API structure`

---

## 3. TDD Process

### 3.1 The Red-Green-Refactor Cycle

```
┌─────────────────────────────────────────────────────────────────────┐
│                    RED → GREEN → REFACTOR                           │
│                                                                     │
│  RED    Write the test first. Run it — it MUST FAIL.               │
│         This proves the test is actually testing something new.     │
│         Commit: test(#2): RED - ...                                │
│                                                                     │
│  GREEN  Write the MINIMUM code to make the test PASS.              │
│         No over-engineering. No extra features.                     │
│         Commit: feat(#2): GREEN - ...                              │
│                                                                     │
│  REFACTOR  Improve the code. Add docstrings. Extract helpers.      │
│         Run tests again — all must still pass.                      │
│         Commit: refactor(#2): ...                                  │
└─────────────────────────────────────────────────────────────────────┘
```

One complete RED-GREEN-REFACTOR cycle was executed per API:
- Create Module: 6 tests → 6 passed
- Edit Module: 6 tests → 6 passed
- Delete Module: 5 tests → 5 passed

### 3.2 Test Scenario Coverage Pattern

Every API used the same coverage template:

| Category | Scenario Type | What it proves |
|---|---|---|
| **Happy Path** | Valid payload + correct role | The endpoint works |
| **Validation Error** | Missing or empty required field | Pydantic schema catches bad input |
| **Business Logic** | Duplicate title, ownership check | Service layer enforces invariants |
| **Authentication** | No token sent | JWT guard rejects unauthenticated requests |
| **Authorization** | Wrong role / wrong owner | Fine-grained access control works |

### 3.3 `module_service.py` — The DRY Backbone

A key design decision made during the REFACTOR phase was to extract all business logic into `server/src/services/module_service.py`. This kept route handlers thin (< 5 lines each) and made logic reusable across tests:

```python
# module_service.py — functions used by all 3 APIs
get_module_by_id(db, module_id)         # shared by edit + delete
get_module_by_title(db, instructor_id, title)  # used by create (409 check)
create_module(db, instructor_id, payload)
update_module(db, module_id, instructor_id, payload)  # partial update via exclude_unset
delete_module(db, module_id, instructor_id)
```

The router (`modules.py`) delegates every DB call to the service, ensuring no business logic leaks into HTTP handler code.

### 3.4 Fixtures Design (`conftest.py`)

A shared `conftest.py` provided all three test files with reusable fixtures:

```python
@pytest.fixture
def client() -> TestClient:
    """In-memory test client — no real HTTP, no real DB."""

@pytest.fixture
def instructor_token() -> str:
    """JWT for user_id=1, role='instructor'."""

@pytest.fixture
def student_token() -> str:
    """JWT for user_id=2, role='student'."""

@pytest.fixture
def second_instructor_token() -> str:
    """JWT for user_id=3, role='instructor' — used to test ownership isolation."""
```

The `second_instructor_token` fixture was added specifically to enable the "Wrong Owner" test scenario for both Edit and Delete APIs, validating that **ownership is checked**, not just role.

---

## 4. Git History

### 4.1 Commit Timeline

The full TDD commit sequence for HW4 (branch: `feature/2-instructor-module-api`):

```
chore(#2): init claude code and permissions
    └── CLAUDE.md and .claude/settings.json configured via /init

test(#2): RED - add failing tests for create module API
    └── 6 tests written, all FAIL (route doesn't exist yet)

feat(#2): GREEN - implement create module API to pass tests
    └── Schema + route + service; all 6 tests PASS

refactor(#2): improve create module API structure and update dependencies
    └── Docstrings, DRY helpers, pinned requirements.txt

test(#2): RED - add failing tests for edit module API
    └── 6 tests written, all FAIL

feat(#2): GREEN - implement edit module API to pass tests
    └── PUT route + partial update via exclude_unset; all 6 PASS

refactor(#2): improve edit module API structure
    └── Extract get_module_by_id(), docstring consistency

test(#2): RED - add failing tests for delete module API
    └── 5 tests written, all FAIL (Method Not Allowed)

feat(#2): GREEN - implement delete module API to pass tests
    └── DELETE route + service reusing get_module_by_id(); all 5 PASS

refactor(#2): improve delete module API structure
    └── CRUD ordering, Returns docstring uniformity

docs(#2): add HW4 reflection and logs
    └── Session log, reflection doc, PR created
```

> Screenshot of full git log: `docs/screenshot/08_Final_TDD_commits_history.png`
> Mid-point git log (after Create): `docs/screenshot/03_TDD_commits_history.png`

### 4.2 How Each Commit Represents a TDD Phase

| Commit prefix | TDD Phase | Why it matters |
|---|---|---|
| `test(#2): RED` | RED — tests written, must fail | Proves tests were written **before** implementation |
| `feat(#2): GREEN` | GREEN — minimal implementation | Proves tests drove the implementation |
| `refactor(#2):` | REFACTOR — quality pass | Proves the cycle completes without breaking anything |

The commit message convention (`test`, `feat`, `refactor`) + the Issue ID (`#2`) + the phase label (`RED`, `GREEN`) in the message body creates a searchable, auditable record of the entire TDD workflow directly in git history.

---

## 5. Test Results

### 5.1 Final Pytest Output (All Tests Passing)

After all three APIs were implemented and refactored, the full backend test suite runs clean:

```
============================================================ test session starts ============================================================
platform darwin -- Python 3.12.0, pytest-9.0.2, pluggy-1.6.0
rootdir: /Users/melaniey/Github/LearnMateAI
configfile: pytest.ini
plugins: cov-7.1.0, asyncio-0.21.1, anyio-3.7.1
asyncio: mode=Mode.STRICT
collected 17 items

tests/backend/test_create_module.py ......  [ 35%]
tests/backend/test_edit_module.py   ......  [ 71%]
tests/backend/test_delete_module.py .....   [100%]

============================================================ 17 passed in 0.14s =============================================================
```

### 5.2 Test Count Summary

| Test File | Tests | Status |
|---|---|---|
| `test_create_module.py` | 6 | All PASSED |
| `test_edit_module.py` | 6 | All PASSED |
| `test_delete_module.py` | 5 | All PASSED |
| **Total** | **17** | **17 PASSED** |

### 5.3 Screenshot Evidence Index

| Screenshot | Phase | API |
|---|---|---|
| `01_RED_phase_failing_tests.png` | RED | Create Module |
| `02_01_GREEN_phase_passed.png` | GREEN | Create Module |
| `02_02_GREEN_phase_passed_summary_from_claude.png` | GREEN | Create Module (Claude summary) |
| `03_TDD_commits_history.png` | Git Log | After Create complete |
| `04_Edit_RED_phase_failing_tests.png` | RED | Edit Module |
| `05_Edit_GREEN_phase_passed.png` | GREEN | Edit Module |
| `06_Delete_RED_phase_failing_tests.png` | RED | Delete Module |
| `07_Delete_GREEN_phase_passed.png` | GREEN | Delete Module |
| `08_Final_TDD_commits_history.png` | Git Log | Full TDD history |

---

## Reflection

### How the Explore → Plan → Implement → Commit Workflow Changed Our Approach

Before using Claude Code, the natural tendency was to jump directly into implementation: open a file, start writing code, fix errors as they appear. The Explore → Plan → Implement → Commit discipline enforces a fundamentally different cadence.

**Explore** with Glob/Grep/Read first meant Claude always understood the existing architecture before touching anything. This eliminated a common mistake: writing new code that duplicated what already existed (e.g., `get_module_by_id()` was discovered to already exist during the Edit API's Explore phase, preventing a copy-paste bug).

**Plan mode** forced articulation of the approach in plain language before any code was written. When Claude stated the TDD plan for Delete ("all 5 tests will fail with 404 Method Not Allowed"), it was immediately clear what the RED terminal output *should* look like — making the actual test run interpretable, not surprising.

**Commit discipline** turned git history into a readable story. Rather than a blob of "add modules feature" commits, the history explicitly maps every test, implementation, and cleanup step to a phase label and Issue ID.

### Context Management

The most effective strategy was `/compact` between major phases (e.g., between finishing Create and starting Edit). This prevented token bloat from early exploratory output from polluting the implementation conversation. The `--continue` flag was used to resume across days without losing the current feature context.

The `@import` directives in `CLAUDE.md` (importing the Sprint Plan and proposal) meant Claude always had high-level project goals available as persistent context, without needing to re-explain the architecture at the start of each session.
