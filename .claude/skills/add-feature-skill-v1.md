# Claude Code Skill: /add-feature (v1)

## Metadata
**Name:** `/add-feature`  
**Version:** 1.0  
**Purpose:** Add new features to P3 project with full TDD + documentation  
**Status:** Initial Implementation  
**Created:** March 28, 2026  
**Based On:** HW4's `/tdd-feature` skill (extended)

---

## Overview

The `/add-feature` skill automates full-stack feature development:

1. **EXPLORE** - Understand existing code patterns
2. **PLAN** - Design the feature approach  
3. **RED** - Write failing tests (TDD)
4. **GREEN** - Implement minimum code
5. **REFACTOR** - Improve code quality
6. **COMMIT** - Create clean git history
7. **DOCUMENT** - Update API/feature docs

This skill is optimized for LearnMateAI's full-stack development (FastAPI backend + React frontend).

---

## Usage

```bash
/add-feature <feature-name> <acceptance-criteria>
```

### Examples

```bash
# Simple feature
/add-feature "Student Notes Upload" "1. Upload notes to module, 2. Store in database, 3. Show success message"

# Complex feature  
/add-feature "Quiz Generation" "1. Generate quiz from module content, 2. Create questions, 3. Add answer options, 4. Calculate difficulty"

# With options
/add-feature "Student Notes" "criteria" --backend --frontend --full-stack
```

---

## 7-Phase Workflow

### Phase 1: EXPLORE (Automatic)

Run Explore commands to understand:
- Existing project structure
- Similar features in codebase
- Architecture patterns
- Naming conventions
- Test patterns

**Commands:**
```bash
glob src/backend/
glob src/frontend/
read src/backend/services/module_service.py (first 50 lines)
read tests/backend/conftest.py
```

**Claude Output:**
```
## EXPLORE Phase Summary

**Project Structure:**
- Backend: FastAPI with SQLAlchemy ORM
- Frontend: React + Vite with TypeScript
- Testing: pytest (backend), vitest (frontend)

**Similar Features Found:**
- Module CRUD (src/backend/services/module_service.py)
- Module routes (src/backend/routers/modules.py)
- Test patterns in tests/backend/

**Naming Conventions:**
- Services: snake_case functions in *_service.py
- Routes: snake_case endpoints in routers/
- Tests: test_*.py with class-based tests
- Models: PascalCase for classes

Ready for PLAN phase.
```

---

### Phase 2: PLAN (Interactive)

Ask for clarification and confirm scope:

```
## PLAN Phase

Feature: "Student Notes Upload"

Confirm this scope:
1. Backend: Create StudentNote model, router, service, schema
2. Frontend: Create upload form component
3. API: POST /api/v1/modules/{id}/notes endpoint
4. Database: student_notes table with FK to modules
5. Tests: 6 backend tests + 3 frontend tests

Is this correct? (yes/no/modify)
```

If user confirms, provide:
- Architecture diagram
- File list to create/modify
- Test count estimate
- Time estimate

---

### Phase 3: RED (Test-First)

Write **only** test files. No implementation code.

**Backend Tests:**
Create `tests/backend/test_student_notes.py`
```python
class TestStudentNotes:
    def test_upload_notes_success(self, test_client, db, student_token, sample_module):
        """Happy path: Student uploads notes to module."""
        response = test_client.post(
            f"/api/v1/modules/{sample_module.id}/notes",
            json={"content": "My study notes..."},
            headers={"Authorization": f"Bearer {student_token}"}
        )
        assert response.status_code == 201
        
    def test_upload_notes_unauthorized(self, test_client, sample_module):
        """Error: Not authenticated."""
        response = test_client.post(f"/api/v1/modules/{sample_module.id}/notes")
        assert response.status_code == 401
    
    def test_upload_notes_module_not_found(self, test_client, student_token):
        """Error: Module doesn't exist."""
        response = test_client.post(
            "/api/v1/modules/99999/notes",
            json={"content": "Notes"},
            headers={"Authorization": f"Bearer {student_token}"}
        )
        assert response.status_code == 404
```

**Frontend Tests:**
Create `src/frontend/src/components/__tests__/StudentNotesForm.test.tsx`
```typescript
describe("StudentNotesForm", () => {
    it("renders upload form", () => {
        render(<StudentNotesForm moduleId={1} />);
        expect(screen.getByRole("textbox")).toBeInTheDocument();
        expect(screen.getByRole("button", { name: /upload/i })).toBeInTheDocument();
    });
    
    it("submits notes on form submission", async () => {
        const mockSubmit = vi.fn();
        render(<StudentNotesForm moduleId={1} onSubmit={mockSubmit} />);
        
        const textarea = screen.getByRole("textbox");
        await userEvent.type(textarea, "My notes");
        await userEvent.click(screen.getByRole("button", { name: /upload/i }));
        
        expect(mockSubmit).toHaveBeenCalledWith("My notes");
    });
});
```

**Run tests to prove they FAIL:**
```bash
pytest tests/backend/test_student_notes.py -v
# Output: 3 FAILED (route not implemented)

npm test -- StudentNotesForm
# Output: 2 FAILED (component doesn't exist)
```

---

### Phase 4: GREEN (Minimum Implementation)

Implement only what's needed to pass tests.

**Backend Implementation:**

1. **Model** (`src/backend/models/student_note.py`):
```python
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from src.backend.database import Base

class StudentNote(Base):
    __tablename__ = "student_notes"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    student_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

2. **Schema** (`src/backend/schemas/student_note.py`):
```python
from pydantic import BaseModel
from datetime import datetime

class StudentNoteCreate(BaseModel):
    content: str

class StudentNoteResponse(BaseModel):
    id: int
    content: str
    module_id: int
    student_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
```

3. **Service** (`src/backend/services/student_note_service.py`):
```python
from sqlalchemy.orm import Session
from src.backend.models.student_note import StudentNote
from src.backend.schemas.student_note import StudentNoteCreate, StudentNoteResponse
from fastapi import HTTPException

def create_student_note(
    db: Session,
    module_id: int,
    student_id: int,
    payload: StudentNoteCreate
) -> StudentNoteResponse:
    """Create a new student note for a module."""
    
    # Verify module exists
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    # Create note
    note = StudentNote(
        content=payload.content,
        module_id=module_id,
        student_id=student_id
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return StudentNoteResponse.from_orm(note)
```

4. **Router** (`src/backend/routers/student_notes.py`):
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.backend.database import get_db
from src.backend.dependencies import require_student
from src.backend.schemas.student_note import StudentNoteResponse, StudentNoteCreate
from src.backend.services import student_note_service

router = APIRouter()

@router.post(
    "/modules/{module_id}/notes",
    response_model=StudentNoteResponse,
    status_code=201
)
def create_student_note(
    module_id: int,
    payload: StudentNoteCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_student)
) -> StudentNoteResponse:
    """Create student notes for a module."""
    student_id = int(current_user["sub"])
    return student_note_service.create_student_note(db, module_id, student_id, payload)
```

**Frontend Implementation:**

Create `src/frontend/src/components/StudentNotesForm.tsx`:
```typescript
import { useState } from "react";
import { FC } from "react";

interface StudentNotesFormProps {
    moduleId: number;
    onSubmit?: (content: string) => void;
}

export const StudentNotesForm: FC<StudentNotesFormProps> = ({ moduleId, onSubmit }) => {
    const [content, setContent] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        
        try {
            const response = await fetch(`/api/v1/modules/${moduleId}/notes`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ content })
            });
            
            if (response.ok) {
                setContent("");
                onSubmit?.(content);
            }
        } finally {
            setIsLoading(false);
        }
    };
    
    return (
        <form onSubmit={handleSubmit}>
            <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Enter your study notes..."
                required
            />
            <button type="submit" disabled={isLoading}>
                {isLoading ? "Uploading..." : "Upload"}
            </button>
        </form>
    );
};
```

**Run tests - all PASS:**
```bash
pytest tests/backend/test_student_notes.py -v
# Output: 3 PASSED

npm test -- StudentNotesForm
# Output: 2 PASSED
```

---

### Phase 5: REFACTOR (Code Quality)

Improve code quality while keeping tests GREEN:

**Backend Refactoring:**
- Add comprehensive docstrings (Google style)
- Add logging
- Improve error messages
- Verify PEP 8 compliance (black, flake8, mypy)
- Extract repeated logic

**Frontend Refactoring:**
- Add TypeScript proper types
- Add proper error handling
- Add loading states
- Add accessibility (aria labels)
- Format with Prettier

**Run tests again - still PASS:**
```bash
pytest tests/backend/test_student_notes.py -v
# Output: 3 PASSED

npm test -- StudentNotesForm
# Output: 2 PASSED
```

---

### Phase 6: COMMIT (Clean History)

Create atomic commits showing progression:

```bash
# Commit 1: Tests
git add tests/backend/test_student_notes.py src/frontend/src/components/__tests__/StudentNotesForm.test.tsx
git commit -m "test(#issue): RED - add student notes upload tests"

# Commit 2: Backend models/schemas
git add src/backend/models/student_note.py src/backend/schemas/student_note.py
git commit -m "feat(#issue): GREEN - add student note model and schema"

# Commit 3: Backend service/router
git add src/backend/services/student_note_service.py src/backend/routers/student_notes.py
git commit -m "feat(#issue): GREEN - add student note service and router"

# Commit 4: Frontend component
git add src/frontend/src/components/StudentNotesForm.tsx
git commit -m "feat(#issue): GREEN - add student notes form component"

# Commit 5: Refactor backend
git add src/backend/services/student_note_service.py src/backend/routers/student_notes.py
git commit -m "refactor(#issue): improve student notes with docstrings and logging"

# Commit 6: Refactor frontend
git add src/frontend/src/components/StudentNotesForm.tsx
git commit -m "refactor(#issue): improve form accessibility and error handling"
```

---

### Phase 7: DOCUMENT (Update Docs)

Update project documentation:

**Update `CODEBASE_DOCUMENTATION.md`:**
```markdown
## Student Notes Feature

### Overview
Students can upload notes to learning modules. Notes are persisted to database.

### API Endpoint
POST /api/v1/modules/{module_id}/notes

Request:
```json
{
  "content": "My study notes..."
}
```

Response (201 Created):
```json
{
  "id": 1,
  "content": "My study notes...",
  "module_id": 1,
  "student_id": 42,
  "created_at": "2026-03-28T10:30:00Z",
  "updated_at": "2026-03-28T10:30:00Z"
}
```

### Files Modified
- Backend: models, schemas, services, routers
- Frontend: components
- Database: new student_notes table
- Tests: 3 backend + 2 frontend tests

### Architecture
- Module CRUD → Student Notes relationship
- Student-specific endpoint (requires student role)
- Full test coverage (6 tests)
```

**Update `README.md` with setup instructions:**
```markdown
## Features

- ✅ Module management (instructor)
- ✅ Student notes upload (new!)
- 🔄 Quiz generation (in progress)
- 🔄 Flashcard generation (planned)
```

**Commit documentation:**
```bash
git add CODEBASE_DOCUMENTATION.md README.md
git commit -m "docs(#issue): add student notes feature documentation"
```

---

## Constraints & Rules

### ✓ ALLOWED Operations
- Read files (glob, grep, read)
- Create test files
- Create model/schema files
- Create service/router files
- Create component files
- Run pytest and npm test
- Run git commands
- Run code formatting/linting

### ✗ NOT Allowed Without Confirmation
- Edit existing feature code (without tests first)
- Delete files
- Edit .env or secrets
- Push to remote
- Merge branches

---

## Decision Tree

```
User: /add-feature "Feature" "criteria"
         ↓
    EXPLORE Phase
    (scan patterns)
         ↓
    PLAN Phase
    "Confirm this scope?" 
    User: yes/no
         ↓
    RED Phase
    (write tests)
    Run: pytest
    User: "Ready for GREEN?"
         ↓
    GREEN Phase
    (implement code)
    Run: pytest
    User: "Ready for REFACTOR?"
         ↓
    REFACTOR Phase
    (improve code)
    Run: pytest
    User: "Ready for COMMIT?"
         ↓
    COMMIT Phase
    (create commits)
         ↓
    DOCUMENT Phase
    (update docs)
         ↓
    ✓ Feature Complete!
```

---

## Real Workflow Example

```
User: /add-feature "Student Notes Upload" "1. Upload notes, 2. Store in DB, 3. Show success"

Claude Code:

## EXPLORE Phase
✓ Analyzing project structure...
✓ Found backend patterns: services, routers, models
✓ Found frontend patterns: components, hooks
✓ Found test patterns: pytest for backend, vitest for frontend
✓ Database: PostgreSQL with SQLAlchemy

## PLAN Phase

Feature: Student Notes Upload

Scope:
1. Backend: StudentNote model, service, router
2. Frontend: StudentNotesForm component
3. Tests: 3 backend + 2 frontend
4. Database: student_notes table
5. API: POST /api/v1/modules/{id}/notes

Confirm? (yes/no)

---

User: yes

---

Claude Code:

## RED Phase

Creating test files:
✓ tests/backend/test_student_notes.py (3 tests)
✓ src/frontend/src/components/__tests__/StudentNotesForm.test.tsx (2 tests)

Running: pytest tests/backend/test_student_notes.py -v

FAILED test_upload_notes_success (404, route missing)
FAILED test_upload_notes_unauthorized (404)
FAILED test_upload_notes_module_not_found (404)

Running: npm test -- StudentNotesForm

FAILED StudentNotesForm renders form
FAILED StudentNotesForm submits notes

✓ All 5 tests FAILED (expected - no implementation yet)

Ready for GREEN? (yes/no)

---

User: yes

---

Claude Code:

## GREEN Phase

Creating backend implementation:
✓ src/backend/models/student_note.py
✓ src/backend/schemas/student_note.py
✓ src/backend/services/student_note_service.py
✓ src/backend/routers/student_notes.py

Creating frontend implementation:
✓ src/frontend/src/components/StudentNotesForm.tsx

Running: pytest tests/backend/test_student_notes.py -v

PASSED test_upload_notes_success
PASSED test_upload_notes_unauthorized
PASSED test_upload_notes_module_not_found

Running: npm test -- StudentNotesForm

PASSED StudentNotesForm renders form
PASSED StudentNotesForm submits notes

✓ All 5 tests PASSED!

Ready for REFACTOR? (yes/no)

---

User: yes

---

Claude Code:

## REFACTOR Phase

Improving code quality...
✓ Added Google-style docstrings
✓ Added logging to service functions
✓ Improved error messages
✓ Added TypeScript proper types
✓ Added form accessibility labels

Running quality checks:
✓ black: 0 issues
✓ flake8: 0 issues
✓ mypy: 0 issues
✓ prettier: 0 issues

Running: pytest tests/backend/test_student_notes.py -v

✓ All 5 tests still PASSED (refactoring safe)

Ready for COMMIT? (yes/no)

---

User: yes

---

Claude Code:

## COMMIT Phase

Creating git history:
✓ test(#issue): RED - add student notes upload tests
✓ feat(#issue): GREEN - add student note model and schema
✓ feat(#issue): GREEN - add student note service and router
✓ feat(#issue): GREEN - add student notes form component
✓ refactor(#issue): improve student notes with docstrings and logging
✓ refactor(#issue): improve form accessibility and error handling

Ready for DOCUMENT? (yes/no)

---

User: yes

---

Claude Code:

## DOCUMENT Phase

Updating documentation:
✓ CODEBASE_DOCUMENTATION.md - Added Student Notes section
✓ README.md - Updated features list
✓ docs(#issue): add student notes feature documentation

✓ Feature Complete!

Git log:
8a7b9c0 docs(#issue): add student notes feature documentation
7f6e5d4 refactor(#issue): improve form accessibility and error handling
6e5d4c3 refactor(#issue): improve student notes with docstrings and logging
5d4c3b2 feat(#issue): GREEN - add student notes form component
4c3b2a1 feat(#issue): GREEN - add student note service and router
3b2a190 feat(#issue): GREEN - add student note model and schema
2a190f8 test(#issue): RED - add student notes upload tests

✓ Ready to push!
```

---

## Success Criteria

The `/add-feature` skill is successful when:

✅ **EXPLORE phase** - Identifies existing patterns correctly  
✅ **PLAN phase** - Confirms scope with user  
✅ **RED phase** - Tests fail initially (proven by pytest)  
✅ **GREEN phase** - Tests pass with minimum code  
✅ **REFACTOR phase** - Code is clean, tests still pass  
✅ **COMMIT phase** - 6+ focused commits created  
✅ **DOCUMENT phase** - Docs updated and committed  

---

## Version History

### v1.0 (Initial - This File)
- 7-phase workflow: Explore-Plan-Red-Green-Refactor-Commit-Document
- Full-stack support (backend + frontend)
- Interactive decision points
- TDD enforcement
- Documentation step
- Atomic commits
- Based on proven HW4 `/tdd-feature` skill

### v2.0 (Planned Improvements)
- Smart template generation
- Parallel feature support
- Mutation testing
- Automated dependency analysis
- Better error recovery
- Performance profiling
- Integration test support

