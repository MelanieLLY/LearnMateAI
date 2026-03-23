# HW4 Reflection: Claude Code Workflow

## Part 1: Explore→Plan→Implement→Commit Workflow

### How Claude Code is Different

Previously we worked like this:
- Plan in Claude Web 
- Hand off concise prompts to Antigravity
- Review output quality before committing
- Work separately on different tasks (send work, wait for feedback)
- Then start coding

Now with Claude Code:
- **EXPLORE** - Read existing code in terminal
- **PLAN** - Write down what we'll do (while looking at code)
- **IMPLEMENT** - Write tests first, then code
- **COMMIT** - Save with clear messages

### Why This is Better

**No context switching:** Everything happens in Claude Code terminal. No jumping between chat, Antigravity, and our IDE.

**Real-time feedback:** We see code as we build it. We can test immediately.

**Better coordination:** We work in same Claude Code session. We give test descriptions, Claude writes tests, tests fail, Claude implements, tests pass, we refactor together.

**Faster:** Old way: 4-5 hours per feature. New way: 1 hour per feature.

---

## Part 2: The 4 Steps

### STEP 1: EXPLORE

Read existing code to understand patterns:
- Find all TypeScript files
- Find where quiz code already exists
- Read how existing functions work

Result: We know what exists. We don't build it twice.

---

### STEP 2: PLAN

Write down the approach while looking at actual code:

**Goal:** Students make AI quizzes from notes

**What we'll do:**
- Create generateQuiz() function
- Add POST /api/quizzes endpoint
- Write tests first

**Reuse existing:**
- Use generateContent() (already exists)
- Same error handling pattern
- Same TypeScript types

**Potential issues:**
- AI questions might be bad (add validation)
- Slow API calls (add caching)

Result: Clear roadmap. Everyone knows the plan.

---

### STEP 3: IMPLEMENT (Red-Green-Refactor)

**RED: Write test that fails**

We write a test for the quiz generation function. When we run the test, it fails because the function doesn't exist yet.

Result: ✗ Test fails (expected)

**GREEN: Write minimum code**

We write the quiz generation function with the minimum code needed to make the test pass. When we run the test again, it passes.

Result: ✓ Test passes

**REFACTOR: Make it real**

We improve the code by replacing fake data with the real Claude API. We run the test again to make sure it still passes.

Result: ✓ Test passes (better code)

**Result:** Tests prove code works. We're confident.

---

### STEP 4: COMMIT

Save work with clear messages:
- Commit 1: "add quiz generation test"
- Commit 2: "implement quiz generation"
- Commit 3: "add real Claude API"

Result: Clean git history. Anyone can understand what we did.

---

## Part 3: Context Management Strategies

### Strategy 1: CLAUDE.md File

One file that explains the entire project:
- Tech Stack: Node.js + React + PostgreSQL + Claude API
- File Structure: where code lives (routes, services, models)
- How We Build: patterns everyone follows
- Rules: DOs and DON'Ts

Why it works: New Claude Code session reads CLAUDE.md automatically. No need to explain project again. Saves 15 minutes per session.

---

### Strategy 2: Use /compact and /clear

After 30 minutes, Claude Code gets slow.

**Solution:**
- Use /compact command: Claude keeps important information and removes old messages
- Use /clear command: Fresh start for next feature (git history saved)

Why it works: Keeps sessions fast. One feature per session equals focused work.

---

### Strategy 3: Real-Time Coordination

We both work in same Claude Code session:
- One person drives (writes code)
- Other person navigates (watches and gives feedback)
- We can switch roles instantly
- No "send and wait" - we decide together in real-time

Result: Better decisions. Fewer mistakes.

---

## Part 4: Real Session Example

### Feature: Instructor Module Management API (CRUD Operations)

We built 3 APIs using TDD for Issue #2: Create Module, Edit Module, Delete Module.

**SESSION 1: Project Setup with /init**

Claude reviewed CLAUDE.md and fixed issues:
- Updated for FastAPI (was Next.js references)
- Added Python conventions (PEP 8, type hints, docstrings)
- Fixed .claude/settings.json permissions for allowed commands

Result: ✓ Project ready for TDD

---

**SESSION 2: Create Module API**

EXPLORE (5 min)
- Use Glob, Grep, Read to understand FastAPI routes structure
- Find existing schemas and test patterns

PLAN (5 min)
- Red: Write 6 failing tests (happy path, missing title, duplicate, auth)
- Green: Implement minimum code
- Refactor: Add docstrings, update dependencies

RED PHASE (10 min)

We gave Claude test descriptions:
- Happy Path: Successfully create module with valid payload, Expect 201
- Missing Title: Fail to create without required field, Expect 422
- Duplicate Title: Fail if same instructor creates duplicate, Expect 409 Conflict
- Unauthorized: Fail if not authenticated or not instructor, Expect 401/403

Claude wrote the failing tests based on our descriptions.

Result: 6 tests failed (expected - API doesn't exist yet)
Evidence: Pytest output shows all 6 tests failed as expected

GREEN PHASE (15 min)

Implement:
- ModuleCreate schema (FastAPI Pydantic)
- create_module() route in routers/modules.py
- Check auth, validate title, prevent duplicates

Result: ✓ 6 tests passed

REFACTOR PHASE (10 min)

- Follow PEP 8 style
- Add docstrings for schema and route
- Extract logic to module_service.py
- Update requirements.txt (latest stable versions)

Result: ✓ 6 tests passed (still good)

Commits:
- test(#2): RED - add failing tests for create module
- feat(#2): GREEN - implement create module API
- refactor(#2): improve create module structure

---

**SESSION 3: Edit Module API**

EXPLORE (5 min)
- Review how Create Module implemented (schemas, routes)
- Plan reuse patterns

PLAN (5 min)
- Red: Write 6 failing tests (happy path, not found, auth, ownership)
- Green: Implement minimum edit_module()
- Refactor: Add get_module_by_id() service, docstrings

RED PHASE (10 min)

We gave Claude test descriptions:
- Happy Path: Successfully edit module title/description, Expect 200
- Not Found: Try to edit non-existent module, Expect 404
- Unauthorized: Not the owner or not authenticated, Expect 401/403

Claude wrote the failing tests based on our descriptions.

Result: 6 tests failed (expected - endpoint missing)
Evidence: Pytest output shows all 6 tests failed as expected

GREEN PHASE (15 min)

Implement:
- ModuleUpdate schema
- update_module() route
- Owner check + validation

Result: ✓ 6 tests passed

REFACTOR PHASE (10 min)

- Extract get_module_by_id() helper (reuse pattern from Create)
- PEP 8 compliance
- Match docstring style from Create API

Result: ✓ 6 tests passed

Commits:
- test(#2): RED - add failing tests for edit module
- feat(#2): GREEN - implement edit module API
- refactor(#2): improve edit API and add get_module_by_id()

---

**SESSION 4: Delete Module API**

EXPLORE (5 min)
- Check existing delete patterns in codebase
- Review db schemas for cascade rules

PLAN (5 min)
- Red: Write 5 failing tests (success, not found, auth, ownership)
- Green: Implement delete_module() route (status 204, no body)
- Refactor: Add docstrings, consistent error handling

RED PHASE (10 min)

We gave Claude test descriptions:
- Happy Path: Successfully delete module, Expect 200/204
- Not Found: Try to delete non-existent module, Expect 404
- Unauthorized: Not the owner or not authenticated, Expect 401/403

Claude wrote the failing tests based on our descriptions.

Result: 5 tests failed (expected - endpoint missing)
Evidence: Pytest output shows all 5 tests failed as expected

GREEN PHASE (15 min)

Implement:
- delete_module() route (DELETE /modules/{module_id})
- Call module_service.delete_module()
- Return 204 (No Content)

Result: ✓ 5 tests passed

REFACTOR PHASE (10 min)

- Reorder functions in module_service.py (CRUD sequence)
- Add Returns section to delete_module docstring (consistency)
- PEP 8 compliance

Result: ✓ 5 tests passed

Commits:
- test(#2): RED - add failing tests for delete module
- feat(#2): GREEN - implement delete module API
- refactor(#2): improve delete API and docstrings

---

**TOTAL RESULTS: 3 APIs Complete**

17 tests written first (RED)
All 17 tests pass (GREEN)
Code refactored (REFACTOR)
9 clean commits (clear history)

All session logs documented in claude-log.md with:
- Complete user prompts and Claude responses
- Pytest output showing RED, GREEN, REFACTOR phases
- Screenshot evidence for each major phase
- Clear annotations of what happened and why

Commits:
- test(#2): RED - add failing tests for create module
- feat(#2): GREEN - implement create module API
- refactor(#2): improve create module structure
- test(#2): RED - add failing tests for edit module
- feat(#2): GREEN - implement edit module API
- refactor(#2): improve edit API and docstrings
- test(#2): RED - add failing tests for delete module
- feat(#2): GREEN - implement delete module API
- refactor(#2): improve delete API and docstrings

What helped:
- CLAUDE.md (context every session)
- /init setup (fixed permissions, conventions)
- /compact (kept sessions focused)
- Explored first (reused patterns: get_module_by_id())
- Planned before coding (knew what to test)
- Tests first (17 tests, 100% pass rate)

---

## Summary

### The Workflow is Faster

| Item | Time |
|------|------|
| One feature (old way) | 4-5 hours |
| One feature (new way) | 1 hour |
| Time saved | 3-4 hours |
| **10 features total** | **30-40 hours saved** |

That's a whole week of work saved.

---

### Why It Works

1. **Explore first** - We don't build same thing twice
2. **Plan before code** - No confusion during coding
3. **Tests first** - Code works or we see it immediately
4. **Clean commits** - Git history tells the story
5. **Real-time teamwork** - We work together, not in sequence

---

### Key Learning

Claude Code is the opposite of our old workflow:
- Old: Plan in chat → Hand off to tool → Review → Coordinate → Code
- New: Explore → Plan → Implement → Commit (all in one place)

Result: Faster, clearer, better teamwork.

---

**Written by:** @Liuyi & @Jing Ng  
**Date:** March 22, 2026  
**Course:** Advanced AI Development
