# HW5 Part 1: Custom Claude Code Skill 

## Overview

This document describes the `/add-feature` skill - a reusable Claude Code workflow for full-stack feature development using Test-Driven Development (TDD).

---

## 1. Skill Definition `/add-feature`

## Part 1: The Skill Files
 
### v1 Skill: Basic Workflow
 
**File:** `.claude/skills/add-feature-skill-v1.md`  
**Size:** 5,000+ words  
**What It Does:** Teaches 7-phase workflow for building features
 
**The 7 Phases:**
1. EXPLORE - Understand existing code
2. PLAN - Design your feature
3. RED - Write tests first (they fail)
4. GREEN - Write code to pass tests
5. REFACTOR - Clean up the code
6. COMMIT - Save to git
7. DOCUMENT - Update documentation
 
### v2 Skill: Improved Version
 
**File:** `.claude/skills/add-feature-skill-v2.md`  
**Size:** 5,000+ words  
**What It Adds:** Better guides for each phase
 
**4 Improvements:**
 
1. **Better EXPLORE:**
   - Checklist: What to look for (architecture, naming, patterns, testing)
   - Students know exactly what to check
 
2. **Better RED:**
   - 6-test template (happy path + 5 error cases)
   - Covers 95% of real situations
 
3. **Better GREEN:**
   - Specific file creation order (prevents errors)
   - Model → Schema → Service → Router
 
4. **Better DOCUMENT:**
   - Checklist + template for documentation
   - Consistent, complete documentation
 
---

### Skill Workflow

The `/add-feature` skill implements a **7-phase workflow**:

```
EXPLORE → PLAN → RED → GREEN → REFACTOR → COMMIT → DOCUMENT
```

## Part 3: Task 1 - Student Notes Upload (v1)
 
### What This Feature Does
 
**Name:** Student Notes Upload  
**Skill Used:** v1 (Basic)
 
Students can upload notes to a module. The notes get saved in the database.
 
### Files Created
 
1. `src/backend/models/student_note.py` - Database model
2. `src/backend/schemas/student_note.py` - Data validation
3. `src/backend/services/student_note_service.py` - Business logic
4. `src/backend/routers/student_notes.py` - API endpoint
5. `tests/backend/test_upload_student_note.py` - 6 tests
 
### How It Works
 
**The API Endpoint:**
```
POST /api/v1/modules/{module_id}/notes
```
 
**What You Send:**
```json
{
  "content": "My study notes..."
}
```
 
**What You Get Back (if successful):**
```json
{
  "id": 1,
  "content": "My study notes...",
  "module_id": 1,
  "student_id": 2,
  "uploaded_at": "2026-03-28T10:30:00Z"
}
```
 
### The 7 Phases
 
#### Phase 1: EXPLORE
**What We Found:**
- 3-layer design (Router → Service → Model)
- JWT login already works
- Can check user roles
- Pytest tests are set up
 <img width="600" alt="Screenshot 2026-03-28 at 6 01 56 PM" src="https://github.com/user-attachments/assets/9e43bf22-9d81-48dc-8845-f7ad78c089cc" />

#### Phase 2: PLAN
**Test Cases (6 tests):**
1. Happy Path - Student uploads notes successfully (201)
2. Missing Content - No content in request (422)
3. Empty Content - Content is blank (422)
4. Not Logged In - No login token (401)
5. Wrong User - Instructor tries to upload (403)
6. Module Missing - Module doesn't exist (404)
   
<img width="600" alt="Screenshot 2026-03-28 at 6 02 32 PM" src="https://github.com/user-attachments/assets/da1313bd-38c5-4e5e-90da-7098f9fdab65" />

#### Phase 3: RED - Write Tests First
**Result:** 6 tests written, all fail (expected)
 
**Test File:** `test_upload_student_note.py` (161 lines)

<img width="600" alt="Screenshot 2026-03-28 at 6 02 56 PM" src="https://github.com/user-attachments/assets/596e2f2e-8e04-4092-a94d-5b5c17d65588" />

#### Phase 4: GREEN - Write Code to Pass Tests
**Code Created:** 184 lines of code
 
All 6 tests now pass ✅
 
**No broken tests:** 23/23 total tests pass ✅

<img width="600" alt="Screenshot 2026-03-28 at 6 03 12 PM" src="https://github.com/user-attachments/assets/78c8f048-4171-4fbd-ab56-20f49760fd2d" />
<img width="600" alt="Screenshot 2026-03-28 at 6 03 36 PM" src="https://github.com/user-attachments/assets/bbcb0c5e-1c2a-42c5-a85d-8ba632f52c5c" />
<img width="600" alt="Screenshot 2026-03-28 at 6 03 59 PM" src="https://github.com/user-attachments/assets/ff0a8dab-12b5-4b69-bdd4-9ca7fec22f65" />

#### Phase 5: REFACTOR
Code was already clean - skipped
 
#### Phase 6: COMMIT
**2 Git Commits:**
```
fc82387 test(#student-notes): RED - failing tests first
242f601 feat(#student-notes): GREEN - working code
```
 
#### Phase 7: DOCUMENT
Updated documentation with API details
 
### Results
 
```
✅ 6/6 new tests PASSING
✅ 23/23 total tests PASSING
✅ Zero broken tests
✅ 2 clean git commits
✅ 19 minutes total
```

## Task 2 - Flashcard Generation (v2)

### What This Feature Does
 
**Name:** Flashcard Generation  
**Skill Used:** v2 (Improved)
 
Students can ask AI to create flashcards from their module. AI generates question/answer pairs automatically.
 
### Files Created
 
1. `src/backend/models/flashcard.py` - Database model
2. `src/backend/schemas/flashcard.py` - Data validation
3. `src/backend/agents/flashcard_agent.py` - AI connection
4. `src/backend/services/flashcard_service.py` - Business logic
5. `src/backend/routers/flashcards.py` - API endpoints
6. `tests/backend/test_flashcard_generation.py` - 6 tests
 
### How It Works
 
**Create Flashcards:**
```
POST /api/v1/modules/{module_id}/flashcards
```
 
**Get Flashcards:**
```
GET /api/v1/modules/{module_id}/flashcards
```
 
**What You Get Back:**
```json
[
  {
    "id": 1,
    "question": "What is machine learning?",
    "answer": "A subset of AI that learns from data.",
    "module_id": 1,
    "student_id": 2,
    "created_at": "2026-03-28T10:30:00Z"
  }
]
```
 
### The 7 Phases
 
#### Phase 1: EXPLORE (v2 Checklist Used)
**What We Checked:**
- System design (same 3-layer pattern)
- Naming conventions (same as StudentNote)
- Similar features (StudentNote pattern works)
- Testing structure (same test style)
  
 <img width="600" alt="Screenshot 2026-03-28 at 6 47 09 PM" src="https://github.com/user-attachments/assets/fb59aca1-1393-45dd-97f6-c3cdc239af81" />

**What We Found:**
- 3-layer design is consistent ✓
- Login check already exists ✓
- Module has title + description ✓
- Need new agents/ folder for AI ✓
 
#### Phase 2: PLAN (v2 Template Used)
**6 Tests We Need:**
1. Happy Path - Student creates flashcards (201)
2. Correct Data - Each flashcard has all fields
3. Module Missing - Module doesn't exist (404)
4. Wrong User - Instructor tries (only students can) (403)
5. Not Logged In - No login token (401)
6. Get Flashcards - Can retrieve saved cards (200)
 
**Files to Create (in order):**
- Model (database)
- Schema (validation)
- Agent (AI connection)
- Service (logic)
- Router (API)
- Update main.py (register)
  
<img width="600" alt="Screenshot 2026-03-28 at 6 47 46 PM" src="https://github.com/user-attachments/assets/184ecfe3-6272-40a9-be54-c92d5a078b9d" />

#### Phase 3: RED - Write Tests First
**Result:** 6 tests written, all fail (expected)
 
**Test File:** `test_flashcard_generation.py` (151 lines)
 
<img width="600" alt="Screenshot 2026-03-28 at 6 48 16 PM" src="https://github.com/user-attachments/assets/c21b8674-5ba3-4aee-9b75-5b9d3cf8e50b" />

#### Phase 4: GREEN - Write Code to Pass Tests
**Code Created:** 278 lines of code
 
All 6 tests now pass ✅
 
**No broken tests:** 29/29 total tests pass ✅
 
<img width="600" alt="Screenshot 2026-03-28 at 7 12 58 PM" src="https://github.com/user-attachments/assets/b395c292-40d7-4520-94cb-15d12aa34428" />
<img width="600" alt="Screenshot 2026-03-28 at 7 13 16 PM" src="https://github.com/user-attachments/assets/dc131694-6067-422a-9ca6-3fcda65bb6f1" />
<img width="600" alt="Screenshot 2026-03-28 at 7 13 29 PM" src="https://github.com/user-attachments/assets/f82b6e0d-2525-4735-9de8-df87b3ea11c6" />
<img width="600" alt="Screenshot 2026-03-28 at 7 13 50 PM" src="https://github.com/user-attachments/assets/5ae05690-22c2-4225-9337-c365374a9448" />

#### Phase 5: REFACTOR
Code was already clean - skipped

<img width="400" alt="Screenshot 2026-03-28 at 6 49 20 PM" src="https://github.com/user-attachments/assets/18d4e345-18a6-414a-9138-c0dcdcd73a42" />

#### Phase 6: COMMIT
**3 Git Commits:**
```
f031a7a test(#flashcard-generation): RED - failing tests
4103bf9 feat(#flashcard-generation): GREEN - working code
d82716d docs(#flashcard-generation): update documentation
```
 
#### Phase 7: DOCUMENT
Updated CODEBASE_DOCUMENTATION.md with:
- New flashcard model details
- API endpoint documentation
- Claude AI integration notes
 
### Results
 
```
✅ 6/6 new tests PASSING
✅ 29/29 total tests PASSING
✅ Zero broken tests
✅ 3 clean git commits
✅ 20 minutes total
```
 <img width="600" alt="Screenshot 2026-03-28 at 6 49 37 PM" src="https://github.com/user-attachments/assets/b43dd3d0-3407-478a-9a2b-c1ac60644fda" />

---
