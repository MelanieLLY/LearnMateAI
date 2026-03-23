# HW4 Reflection: Claude Code Workflow

## Part 1: How Claude Code Changed Our Workflow

### The Old Way

Before we used Claude Code:
- We wrote our plan in Claude Web
- We sent prompts to Antigravity tool
- We reviewed the output
- We worked separately from each other
- Then we started coding

### The New Way (Explore-Plan-Implement-Commit)

Now with Claude Code in terminal:
- **EXPLORE** - Read existing code first
- **PLAN** - Decide what to build
- **IMPLEMENT** - Write tests, then code, then improve
- **COMMIT** - Save our work with clear messages

### Why This is Better

**No switching between tools:** Everything happens in Claude Code terminal.

**See code immediately:** We test right away, not later.

**Work together:** We give Claude descriptions, Claude writes code, we both check it.

**Faster:** Old way took 4-5 hours. New way takes 1 hour.

---

## Part 2: What We Actually Did

### Session 1: Project Setup

We asked Claude to check our CLAUDE.md file.

Claude found problems:
- File said "Next.js" but we use Vite/React
- File said "Prisma" but we use FastAPI/Python
- Permission settings were wrong format

Claude fixed everything and updated the settings file.

Result: Project ready to use Claude Code

---

### Session 2: Context Management

We used /compact command.

Claude kept important files:
- CLAUDE.md
- Settings file
- Planning documents

Claude removed old messages.

Result: Session stayed fast and organized

---

### Session 3: Explore and Plan

We said: "Let's work on Issue #2 (Instructor Module Management API)"

Claude used Explore tools:
- Found FastAPI routes
- Found existing schemas
- Found test patterns

Claude made a plan:
- RED phase: Write 6 failing tests
- GREEN phase: Write code to pass tests
- REFACTOR phase: Make code better
- Plan showed 3 commits (one per phase)

---

### Session 4-5: Create Module API

**RED PHASE (Tests Fail First)**

We told Claude what tests should check:
1. Happy Path: Create module successfully, expect 201
2. Missing Title: Fail without title, expect 422
3. Duplicate Title: Fail if title exists, expect 409
4. Unauthorized: Fail if not authenticated, expect 401/403
5. Empty Title: Also test empty
6. Student Role: Test role-based access

Claude wrote all 6 tests.

Tests ran: All 6 failed (expected - no code yet)
Pytest output: "6 failed in 0.11s"

**GREEN PHASE (Tests Pass)**

Claude implemented:
- Created ModuleCreate schema
- Built create_module() route
- Added auth checking
- Added duplicate title checking
- Added required field validation

Tests ran: All 6 passed
Pytest output: "6 passed, 4 warnings in 0.07s"

**REFACTOR PHASE (Make Better)**

Claude improved code:
- Fixed PEP 8 style
- Added docstrings
- Updated requirements.txt

Tests ran: All 6 still passed

Git commits made:
- test(#2): RED - add failing tests for create module
- feat(#2): GREEN - implement create module API
- refactor(#2): improve create module API structure

---

### Session 6.5-9: Edit Module API

Same pattern as Create:

Claude reviewed how we built Create API (schemas, routes).

Claude made plan for Edit API:
- RED: 6 tests fail
- GREEN: 6 tests pass
- REFACTOR: Improve code

Tests written: 6 tests for edit scenarios
- Edit successfully, expect 200
- Edit non-existent, expect 404
- Unauthorized edit, expect 401/403
- Partial updates
- Wrong instructor
- Student cannot edit

RED: 6 tests failed (as expected)
GREEN: 6 tests passed (all working)
REFACTOR: 
- Extracted get_module_by_id() helper function
- Added consistent docstrings
- Tests: 6 passed

---

### Session 10-13: Delete Module API

Claude checked Delete API plan:
- 5 tests needed (success, not found, unauthorized, ownership, wrong instructor)
- Delete route status 204 (no content returned)
- Reuse get_module_by_id() pattern

**RED PHASE:** 5 tests written and failed (no endpoint yet)
Pytest: "5 failed in 0.08s"

**GREEN PHASE:** Code implemented
- delete_module() function in service
- DELETE endpoint in routes
- Returns 204 (empty response)

Tests: 5 passed
Pytest: "5 passed in 0.04s"

**REFACTOR PHASE:**
- Reordered functions (CRUD sequence: get, create, update, delete)
- Added Returns section to docstring
- Tests: 5 passed

---

## Part 3: Context Management Strategies That Worked

### Strategy 1: CLAUDE.md File

One file with project information:
- Tech Stack: Vite/React frontend, FastAPI backend
- Files structure (src/**, tests/**)
- Allowed commands (npm, python, pytest, etc.)
- Python rules (PEP 8, type hints, docstrings)

Why: Claude read it automatically, no need to re-explain each session.

Saved 15 minutes per session.

---

### Strategy 2: Use /compact Command

After working 30 minutes, Claude keeps:
- Important files
- Recent progress
- Removes old messages

Why: Session stays fast. Not too much information.

---

### Strategy 3: One Feature Per Session

Work on one API endpoint at a time:
- Create Module session
- Edit Module session
- Delete Module session

Why: Each session stays focused. Easier to understand.

---

### Strategy 4: Work Together in Same Session

One person types the prompt.
Other person reads Claude's response.
Both decide if it's correct.

Why: Better decisions, catch mistakes early.

---

## Part 4: Session Example Summary

### What We Built

3 APIs (Create, Edit, Delete) using TDD

### How Many Tests

Create: 6 tests
Edit: 6 tests
Delete: 5 tests
Total: 17 tests

All tests written first (RED).
All tests passed (GREEN).
Code refactored (REFACTOR).

### Git Commits

All commits follow the pattern:
- test(#2): RED phase
- feat(#2): GREEN phase
- refactor(#2): REFACTOR phase

Each API got 3 commits.
Total: 9 commits showing the workflow.

---

## Summary

### The Workflow is Better

Old way per feature: 4-5 hours
New way per feature: 1 hour
Time saved: 3-4 hours per feature

### Why It Works

1. **Explore first** - Understand existing code
2. **Plan before code** - Know what to build
3. **Tests first** - Code works or we know it fails
4. **Clean commits** - Easy to understand
5. **Work together** - Two people, better decisions

### Key Learning

Claude Code changed our workflow:
- Old: Plan in chat, send to tool, review, coordinate, code
- New: Explore, plan, implement, commit (all in terminal)

Result: Faster, clearer, better teamwork.
