# LearnMateAI Codebase Documentation

**Last Updated:** March 28, 2026  
**Team:** Liuyi, Jing Ng  
**Repository:** https://github.com/MelanieLLY/LearnMateAI  
**Status:** In Development (P3 — due Apr 19, 2026)

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Directory Structure](#directory-structure)
4. [Architecture](#architecture)
5. [Backend Components](#backend-components)
6. [Database Schema](#database-schema)
7. [API Endpoints](#api-endpoints)
8. [Development Workflow](#development-workflow)
9. [Testing Strategy](#testing-strategy)
10. [Coding Conventions](#coding-conventions)
11. [Key Features](#key-features)
12. [Setup & Running](#setup--running)

---

## 🎯 Project Overview

**LearnMateAI** is an AI-powered collaborative learning platform that bridges instructors and students through intelligent content synthesis.

### Core Value Proposition

- **Instructors** upload course materials (lecture notes, slides, documents)
- **Students** upload personal learning notes
- **AI System** synthesizes both sources to generate:
  - Auto-summarized learning content
  - Interactive flashcards
  - Quizzes with adaptive difficulty
  - Anonymous class-wide performance analytics

### MVP Scope

- Module creation and management by instructors
- Multi-tenancy support via user roles (instructor/student)
- JWT-based authentication with bcrypt password hashing
- AI content synthesis via Claude API
- PostgreSQL persistent storage

---

## 🛠️ Tech Stack

### Frontend
- **Framework:** React 19 + Vite
- **Language:** TypeScript (strict mode)
- **Styling:** Tailwind CSS
- **Testing:** Vitest + React Testing Library
- **Build Config:** ESLint, Prettier (100-char width)
- **Port:** http://localhost:5173

### Backend
- **Framework:** FastAPI (Python 3.10+)
- **ORM:** SQLAlchemy
- **Migrations:** Alembic
- **API Validation:** Pydantic
- **Testing:** Pytest (80%+ coverage required)
- **AI:** Claude API (via dedicated agent modules)
- **Database:** PostgreSQL
- **Port:** http://localhost:8000

### DevOps & Infrastructure
- **Monorepo Structure:** Single git repo with `/src/frontend` and `/src/backend`
- **Package Management:** npm (frontend), pip (backend)
- **Environment:** `.env` for secrets (never committed)
- **Version Control:** Git with conventional commits

---

## 📁 Directory Structure

```
LearnMateAI/
├── CLAUDE.md                          # Development guidance for Claude Code
├── CODEBASE_DOCUMENTATION.md          # This file
├── README.md                          # Project overview
├── requirements.txt                   # Python dependencies
├── pytest.ini                         # Pytest configuration
│
├── planning files/
│   ├── homework4_requirement.md       # HW4 specifications
│   ├── homework4_todo.md              # Task tracking for HW4
│   ├── learnmate-sprint-plan.md       # Sprint planning and feature roadmap
│   └── project3_proposal.md           # Project proposal and vision
│
├── docs/
│   ├── claude-log.md                  # Development session logs
│   └── screenshot/                    # UI mockups and screenshots
│
├── src/
│   ├── __init__.py
│   │
│   ├── backend/                       # FastAPI Backend Application
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app instance & router registration
│   │   ├── database.py                # SQLAlchemy engine & Base class
│   │   ├── dependencies.py            # FastAPI dependency injections (JWT, roles)
│   │   │
│   │   ├── models/                    # SQLAlchemy ORM Models
│   │   │   ├── __init__.py
│   │   │   └── module.py              # Module entity (instructor's learning content)
│   │   │
│   │   ├── routers/                   # FastAPI Route Handlers
│   │   │   ├── __init__.py
│   │   │   └── modules.py             # Module CRUD endpoints (/api/v1/modules/*)
│   │   │
│   │   ├── schemas/                   # Pydantic Request/Response Models
│   │   │   ├── __init__.py
│   │   │   └── module.py              # ModuleCreate, ModuleResponse, ModuleUpdate
│   │   │
│   │   ├── services/                  # Business Logic Layer
│   │   │   ├── __init__.py
│   │   │   └── module_service.py      # Module operations (create, read, update, delete)
│   │   │
│   │   └── agents/                    # (Planned) Claude AI Agent Modules
│   │       └── (AI synthesis pipelines)
│   │
│   └── frontend/                      # React Vite Frontend (Not yet in repo)
│       ├── src/
│       │   ├── components/            # React components
│       │   ├── pages/                 # Page-level components
│       │   ├── hooks/                 # Custom React hooks
│       │   ├── utils/                 # Utilities (logger, API client, etc.)
│       │   └── services/              # API service calls
│       └── tests/                     # Vitest test files
│
└── tests/
    ├── __init__.py
    │
    └── backend/                       # Backend Test Suite
        ├── __init__.py
        ├── conftest.py                # Pytest fixtures and configuration
        ├── test_create_module.py      # Tests for module creation
        ├── test_edit_module.py        # Tests for module updates
        └── test_delete_module.py      # Tests for module deletion
```

---

## 🏗️ Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                      │
│                   (Vite, TypeScript, Tailwind)              │
│                                                             │
│  Components → API Client → HTTP Requests → /api/v1/*       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ REST API (JSON)
                     │
┌────────────────────▼────────────────────────────────────────┐
│                    FastAPI Backend                          │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Routers (endpoints)                                 │   │
│  │  - POST /api/v1/modules                             │   │
│  │  - PUT /api/v1/modules/{id}                         │   │
│  │  - DELETE /api/v1/modules/{id}                      │   │
│  │  - GET /api/v1/modules/{id}                         │   │
│  └────────────┬────────────────────────────────────────┘   │
│               │                                             │
│  ┌────────────▼────────────────────────────────────────┐   │
│  │  Dependencies (Auth & Validation)                   │   │
│  │  - require_instructor() → JWT decode & role check   │   │
│  │  - get_db() → Database session injection            │   │
│  └────────────┬────────────────────────────────────────┘   │
│               │                                             │
│  ┌────────────▼────────────────────────────────────────┐   │
│  │  Schemas (Pydantic Models)                          │   │
│  │  - ModuleCreate, ModuleUpdate, ModuleResponse       │   │
│  └────────────┬────────────────────────────────────────┘   │
│               │                                             │
│  ┌────────────▼────────────────────────────────────────┐   │
│  │  Services (Business Logic)                          │   │
│  │  - module_service.create_module()                   │   │
│  │  - module_service.update_module()                   │   │
│  │  - module_service.delete_module()                   │   │
│  └────────────┬────────────────────────────────────────┘   │
│               │                                             │
│  ┌────────────▼────────────────────────────────────────┐   │
│  │  SQLAlchemy ORM & Models                            │   │
│  │  - Module (ORM model representing modules table)    │   │
│  └────────────┬────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ SQL Queries
                     │
┌────────────────────▼────────────────────────────────────────┐
│                  PostgreSQL Database                        │
│                                                             │
│  modules table:                                            │
│  ├── id (INT, PK)                                          │
│  ├── title (VARCHAR, NOT NULL)                             │
│  ├── description (VARCHAR, NULLABLE)                       │
│  ├── instructor_id (INT, NOT NULL)                         │
│  ├── created_at (TIMESTAMP)                                │
│  ├── updated_at (TIMESTAMP)                                │
│  └── UNIQUE(instructor_id, title)                          │
└─────────────────────────────────────────────────────────────┘
```

### Design Principles

1. **Separation of Concerns:** Routers (HTTP) → Services (Logic) → Models (Data)
2. **Dependency Injection:** FastAPI's `Depends()` for auth & database access
3. **Pydantic Validation:** All input validated before business logic
4. **Type Safety:** Full type hints on all Python functions (Python 3.10+)
5. **JWT-based Auth:** Stateless token authentication with role-based access control
6. **Monorepo:** Single repo with clear `/frontend` and `/backend` boundaries

---

## 🔌 Backend Components

### 1. **main.py** - Application Entry Point

**Purpose:** Initialize FastAPI app, create database tables, register routers

**Key Code:**
```python
from fastapi import FastAPI
from src.backend.database import Base, engine
from src.backend.routers.modules import router as modules_router

Base.metadata.create_all(bind=engine)  # Auto-create tables on startup

app = FastAPI(title="LearnMateAI API", version="0.1.0")
app.include_router(modules_router, prefix="/api/v1")
```

**Initialization Flow:**
1. Load environment variables
2. Create SQLAlchemy engine connected to PostgreSQL
3. Create all tables defined in Base metadata
4. Register FastAPI routers under `/api/v1` prefix
5. App ready to receive HTTP requests

---

### 2. **database.py** - Database Configuration

**Purpose:** Manage SQLAlchemy engine, session factory, and Base class

**Key Components:**
- `engine`: SQLAlchemy engine configured with PostgreSQL connection string
- `SessionLocal`: Factory for creating DB sessions
- `Base`: SQLAlchemy declarative base for all ORM models
- `get_db()`: FastAPI dependency that yields a database session

**Example:**
```python
def get_db():
    """Dependency that provides a database session to route handlers."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

### 3. **dependencies.py** - Auth & Validation Middleware

**Purpose:** Implement JWT auth, role-based access control, and injection dependencies

**Key Functions:**
- `require_instructor()`: FastAPI dependency that validates JWT token and ensures user has instructor role
- Additional auth functions (to be expanded): `require_student()`, `require_admin()`, etc.

**Flow:**
1. Extract JWT token from `Authorization: Bearer <token>` header
2. Decode & verify token signature
3. Check user role claim
4. Return decoded payload (with user ID, email, role)
5. Raise `HTTPException(401)` if auth fails; `HTTPException(403)` if insufficient role

---

### 4. **Models** - SQLAlchemy ORM Entities

#### `module.py` - Module Entity

**Purpose:** Represent a course learning module created and managed by an instructor

**Schema:**
```python
class Module(Base):
    __tablename__ = "modules"
    
    id: int (PK, auto-increment)
    title: str (NOT NULL, unique per instructor)
    description: str (NULLABLE)
    instructor_id: int (NOT NULL, FK)
    created_at: datetime (default: now UTC)
    updated_at: datetime (auto-refreshed on update)
    
    # Constraint: unique(instructor_id, title)
```

**Relationships:** (Planned in future sprints)
- One instructor → Many modules
- One module → Many student notes
- One module → Many AI-generated resources

---

### 5. **Schemas** - Pydantic Request/Response Models

#### `module.py` - Module Schemas

**Purpose:** Validate & serialize HTTP request/response payloads

**Key Classes:**

```python
class ModuleCreate(BaseModel):
    """Request body for POST /api/v1/modules"""
    title: str
    description: Optional[str] = None

class ModuleUpdate(BaseModel):
    """Request body for PUT /api/v1/modules/{id}"""
    title: Optional[str] = None
    description: Optional[str] = None

class ModuleResponse(BaseModel):
    """Response body for all module endpoints"""
    id: int
    title: str
    description: Optional[str]
    instructor_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True  # Allow construction from ORM models
```

---

### 6. **Routers** - HTTP Endpoint Handlers

#### `modules.py` - Module CRUD Operations

**Purpose:** Define REST API endpoints for module management

**Endpoints:**

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/api/v1/modules` | Create a new module | ✓ Instructor |
| GET | `/api/v1/modules/{id}` | Retrieve a module by ID | Public |
| PUT | `/api/v1/modules/{id}` | Update module title/description | ✓ Instructor (owner) |
| DELETE | `/api/v1/modules/{id}` | Delete a module | ✓ Instructor (owner) |

**Key Handler Structure:**
```python
@router.post("/modules", response_model=ModuleResponse, status_code=201)
def create_module(
    payload: ModuleCreate,                    # Input validation (Pydantic)
    db: Session = Depends(get_db),           # DB session injection
    current_user: dict = Depends(require_instructor),  # Auth enforcement
) -> ModuleResponse:
    """Route is thin: delegates to service layer."""
    instructor_id = int(current_user["sub"])
    return module_service.create_module(db, instructor_id, payload)
```

---

### 7. **Services** - Business Logic Layer

#### `module_service.py` - Module Operations

**Purpose:** Implement module business logic (CRUD, validation, constraints)

**Key Functions:**

```python
def create_module(
    db: Session,
    instructor_id: int,
    payload: ModuleCreate
) -> ModuleResponse:
    """
    Create a new module owned by an instructor.
    
    Raises:
        - HTTPException(409) if instructor already owns module with this title
        - HTTPException(500) on database error
    """

def update_module(
    db: Session,
    module_id: int,
    instructor_id: int,
    payload: ModuleUpdate
) -> ModuleResponse:
    """
    Update module title/description.
    
    Authorization: Only module owner (instructor) can edit.
    
    Raises:
        - HTTPException(403) if not the owner
        - HTTPException(404) if module doesn't exist
        - HTTPException(409) if new title already exists for this instructor
    """

def delete_module(
    db: Session,
    module_id: int,
    instructor_id: int
) -> None:
    """
    Delete a module.
    
    Authorization: Only module owner can delete.
    
    Raises:
        - HTTPException(403) if not the owner
        - HTTPException(404) if module doesn't exist
    """

def get_module(db: Session, module_id: int) -> ModuleResponse:
    """
    Retrieve a module by ID.
    
    Authorization: Public (any authenticated user can read)
    
    Raises:
        - HTTPException(404) if module doesn't exist
    """
```

---

### 8. **Agents** - AI Integration

**Purpose:** Claude API integration for content synthesis

**Active Modules:**
- `flashcard_agent.py`: Generate flashcards from module content via Claude API

**Planned Modules:**
- `summarizer_agent.py`: Generate summaries from instructor + student notes
- `quiz_agent.py`: Generate adaptive quizzes with difficulty scaling
- `analytics_agent.py`: Analyze performance & generate anonymous reports

**Integration Point:** Agent modules are the single boundary for Claude API calls. Services import agent functions; tests mock at the service module boundary (e.g., `src.backend.services.flashcard_service.generate_flashcards_from_content`).

---

## 📊 Database Schema

### Current Tables

#### `modules`

| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| `id` | INTEGER | PRIMARY KEY, AUTO INCREMENT | Unique module identifier |
| `title` | VARCHAR(255) | NOT NULL | Human-readable module title |
| `description` | TEXT | NULLABLE | Longer module description |
| `instructor_id` | INTEGER | NOT NULL | Instructor owner's user ID |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Creation timestamp (UTC) |
| `updated_at` | TIMESTAMP | DEFAULT NOW(), ON UPDATE | Last update timestamp (UTC) |

**Unique Constraints:**
- `UNIQUE(instructor_id, title)` - No duplicate titles per instructor

#### `student_notes`

| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| `id` | INTEGER | PRIMARY KEY, AUTO INCREMENT | Unique note identifier |
| `content` | TEXT | NOT NULL | Full text of the student's note |
| `module_id` | INTEGER | FK → modules.id, NOT NULL | Module the note belongs to |
| `student_id` | INTEGER | NOT NULL | Student's user ID |
| `uploaded_at` | TIMESTAMP | DEFAULT NOW() | Upload timestamp (UTC) |

#### `flashcards`

| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| `id` | INTEGER | PRIMARY KEY, AUTO INCREMENT | Unique flashcard identifier |
| `question` | TEXT | NOT NULL | Flashcard question generated by AI |
| `answer` | TEXT | NOT NULL | Flashcard answer generated by AI |
| `module_id` | INTEGER | FK → modules.id, NOT NULL | Module the flashcard belongs to |
| `student_id` | INTEGER | NOT NULL | Student who requested generation |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Creation timestamp (UTC) |

**Future Tables (Planned):**
- `users` - Instructors and students (auth, roles, profiles)
- `quiz_attempts` - Student quiz responses for analytics
- `performance_reports` - Aggregated class-wide analytics

---

## 🔌 API Endpoints

### Base URL
```
http://localhost:8000
```

### Authentication
All protected endpoints require:
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

### Module Endpoints

#### 1. Create Module
```http
POST /api/v1/modules
Authorization: Bearer <instructor_jwt>

{
  "title": "Introduction to Machine Learning",
  "description": "Basics of ML, algorithms, and applications"
}
```
**Response (201 Created):**
```json
{
  "id": 1,
  "title": "Introduction to Machine Learning",
  "description": "Basics of ML, algorithms, and applications",
  "instructor_id": 42,
  "created_at": "2026-03-28T10:30:00Z",
  "updated_at": "2026-03-28T10:30:00Z"
}
```
**Error Cases:**
- `401 Unauthorized` - Missing/invalid JWT token
- `403 Forbidden` - User is not an instructor
- `409 Conflict` - Instructor already owns a module with this title
- `422 Unprocessable Entity` - Invalid request body

---

#### 2. Retrieve Module
```http
GET /api/v1/modules/{module_id}
```
**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Introduction to Machine Learning",
  "description": "Basics of ML, algorithms, and applications",
  "instructor_id": 42,
  "created_at": "2026-03-28T10:30:00Z",
  "updated_at": "2026-03-28T10:30:00Z"
}
```
**Error Cases:**
- `404 Not Found` - Module with this ID doesn't exist

---

#### 3. Update Module
```http
PUT /api/v1/modules/{module_id}
Authorization: Bearer <instructor_jwt>

{
  "title": "Advanced Machine Learning",
  "description": "Deep learning, neural networks, transformers"
}
```
**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Advanced Machine Learning",
  "description": "Deep learning, neural networks, transformers",
  "instructor_id": 42,
  "created_at": "2026-03-28T10:30:00Z",
  "updated_at": "2026-03-28T10:45:00Z"
}
```
**Error Cases:**
- `401 Unauthorized` - Missing/invalid JWT token
- `403 Forbidden` - Not the module owner
- `404 Not Found` - Module doesn't exist
- `409 Conflict` - New title conflicts with another of instructor's modules

---

#### 4. Delete Module
```http
DELETE /api/v1/modules/{module_id}
Authorization: Bearer <instructor_jwt>
```
**Response (204 No Content)**
**Error Cases:**
- `401 Unauthorized` - Missing/invalid JWT token
- `403 Forbidden` - Not the module owner
- `404 Not Found` - Module doesn't exist

---

### Student Note Endpoints

#### 5. Upload Student Note
```http
POST /api/v1/modules/{module_id}/notes
Authorization: Bearer <student_jwt>

{
  "content": "My study notes about this topic..."
}
```
**Response (201 Created):**
```json
{
  "id": 1,
  "content": "My study notes about this topic...",
  "module_id": 1,
  "student_id": 2,
  "uploaded_at": "2026-03-28T10:30:00Z"
}
```
**Error Cases:**
- `401 Unauthorized` - Missing/invalid JWT token
- `403 Forbidden` - Not a student
- `404 Not Found` - Module doesn't exist
- `422 Unprocessable Entity` - Empty or missing content

---

### Flashcard Endpoints

#### 6. Generate Flashcards
```http
POST /api/v1/modules/{module_id}/flashcards
Authorization: Bearer <student_jwt>
```
**Response (201 Created):**
```json
[
  {
    "id": 1,
    "question": "What is machine learning?",
    "answer": "A subset of AI that learns from data.",
    "module_id": 1,
    "student_id": 2,
    "created_at": "2026-03-28T10:30:00Z"
  },
  {
    "id": 2,
    "question": "What is a neural network?",
    "answer": "A model inspired by the human brain.",
    "module_id": 1,
    "student_id": 2,
    "created_at": "2026-03-28T10:30:00Z"
  }
]
```
**Error Cases:**
- `401 Unauthorized` - Missing/invalid JWT token
- `403 Forbidden` - Not a student (only students generate flashcards)
- `404 Not Found` - Module doesn't exist

**Notes:** Calls Claude API (`claude-sonnet-4-6`) to generate question/answer pairs from the module title and description. All generated flashcards are persisted to the `flashcards` table.

---

#### 7. Get Flashcards
```http
GET /api/v1/modules/{module_id}/flashcards
Authorization: Bearer <student_jwt>
```
**Response (200 OK):** Same structure as above (list of flashcard objects)

**Error Cases:**
- `401 Unauthorized` - Missing/invalid JWT token
- `403 Forbidden` - Not a student
- `404 Not Found` - Module doesn't exist

---

## 🧪 Testing Strategy

### Testing Overview

| Layer | Framework | Scope | Coverage Target |
|-------|-----------|-------|-----------------|
| Backend Unit Tests | pytest | Service logic, edge cases | 80%+ |
| Backend Integration Tests | pytest | Router → Service → DB | 80%+ |
| Frontend Unit Tests | vitest | Component logic, utilities | 80%+ |
| End-to-End Tests | Playwright/Cypress | Full user workflows | Key paths |

### Backend Test Structure

Location: `/tests/backend/`

#### Test Files

**`conftest.py`** - Shared fixtures
```python
@pytest.fixture
def db():
    """In-memory SQLite test database."""
    # Create test DB, session, cleanup
    
@pytest.fixture
def test_client(db):
    """FastAPI TestClient with test database."""
    
@pytest.fixture
def instructor_token():
    """Valid JWT token for an instructor user."""
    
@pytest.fixture
def student_token():
    """Valid JWT token for a student user."""
```

---

**`test_create_module.py`** - Module creation tests
```python
def test_create_module_success(test_client, instructor_token, db):
    """Test: Instructor can create a module."""
    # POST /api/v1/modules with valid payload
    # Assert: 201, module in DB
    
def test_create_module_unauthenticated(test_client):
    """Test: Unauthenticated request fails."""
    # POST /api/v1/modules without token
    # Assert: 401
    
def test_create_module_non_instructor(test_client, student_token):
    """Test: Student cannot create modules."""
    # POST /api/v1/modules with student JWT
    # Assert: 403
    
def test_create_module_duplicate_title(test_client, instructor_token, db):
    """Test: Cannot create duplicate module title for same instructor."""
    # POST duplicate title for same instructor
    # Assert: 409
```

---

**`test_edit_module.py`** - Update tests
```python
def test_edit_module_success(test_client, instructor_token, db, sample_module):
    """Test: Owner can edit module."""
    
def test_edit_module_non_owner(test_client, instructor_token2, db, sample_module):
    """Test: Non-owner instructor cannot edit."""
    
def test_edit_module_not_found(test_client, instructor_token):
    """Test: 404 for nonexistent module."""
```

---

**`test_delete_module.py`** - Deletion tests
```python
def test_delete_module_success(test_client, instructor_token, db, sample_module):
    """Test: Owner can delete module."""
    
def test_delete_module_non_owner(test_client, instructor_token2, db, sample_module):
    """Test: Non-owner cannot delete."""
```

---

### Running Tests

```bash
# Run all backend tests
pytest tests/backend/

# Run specific test file
pytest tests/backend/test_create_module.py

# Run with coverage
pytest --cov=src/backend --cov-report=term-missing tests/backend/

# Run tests in watch mode
pytest --watch tests/backend/
```

---

## 📝 Coding Conventions

### Python (Backend)

**PEP 8 Strict:**
- 4-space indentation
- 100-character line limit
- `snake_case` for functions, variables, modules
- `PascalCase` for classes
- `UPPER_SNAKE_CASE` for constants

**Type Hints (Required):**
```python
# All function signatures must be type-hinted
def create_module(
    db: Session,
    instructor_id: int,
    payload: ModuleCreate
) -> ModuleResponse:
    """Google-style docstring required."""
    pass
```

**Documentation:**
- Google-style docstrings on all public functions and AI agent modules
- Docstrings include: description, Args, Returns, Raises
- Inline comments for complex logic only (code should be self-documenting)

**Logging (Never `print`):**
```python
import logging
logger = logging.getLogger(__name__)
logger.info("Module created: id=%d, instructor_id=%d", module.id, instructor_id)
```

**No Hardcoded Secrets:**
```python
# ❌ WRONG
API_KEY = "sk-abc123..."
DB_URL = "postgresql://user:pass@localhost/db"

# ✅ CORRECT
import os
API_KEY = os.getenv("CLAUDE_API_KEY")
DB_URL = os.getenv("DATABASE_URL")
```

---

### TypeScript (Frontend)

**Strict Mode (Required):**
```typescript
// tsconfig.json
{
  "compilerOptions": {
    "strict": true  // No `any` types
  }
}
```

**Naming Conventions:**
- Components: `PascalCase` (e.g., `ModuleCard.tsx`)
- Functions/variables: `camelCase` (e.g., `fetchModule()`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `API_BASE_URL`)
- Database tables: `snake_case` (e.g., `modules`, `student_notes`)

**No `any` Types:**
```typescript
// ❌ WRONG
function updateModule(payload: any) {}

// ✅ CORRECT
function updateModule(payload: ModuleUpdate): Promise<Module> {}
```

**Logger Utility:**
```typescript
// ✅ Use logger, never console.log
import { logger } from "src/frontend/utils/logger";
logger.info("Module updated", { moduleId, title });
```

**Formatting:**
- Prettier with 100-character `printWidth`
- Auto-format on save (VSCode)

---

### Git Commit Messages (Conventional Commits)

Format: `<type>(<scope>): <subject> (#<issue>)`

**Types:** `feat`, `fix`, `test`, `refactor`, `docs`, `chore`, `perf`

**Examples:**
```bash
git commit -m "test(module): RED - create_module validation (#5)"
git commit -m "feat(module): GREEN - implement create_module endpoint (#5)"
git commit -m "refactor(module): improve service layer organization (#5)"
git commit -m "docs(api): update endpoint documentation"
```

---

## ✨ Key Features

### Phase 1 (Current - MVP)
- [x] Module CRUD operations (instructor)
- [x] JWT authentication
- [x] Role-based access control (instructor/student)
- [x] Database persistence (PostgreSQL)
- [x] Student note upload (`POST /api/v1/modules/{id}/notes`)
- [x] Flashcard generation via Claude API (`POST /api/v1/modules/{id}/flashcards`)
- [x] Flashcard retrieval (`GET /api/v1/modules/{id}/flashcards`)
- [ ] Basic UI for module management

### Phase 2 (Planned)
- [ ] Claude API integration for summarization
- [ ] Quiz generation with adaptive difficulty
- [ ] Student quiz attempt tracking

### Phase 3 (Planned)
- [ ] Anonymous performance analytics
- [ ] Class-wide insights and reports
- [ ] Teacher dashboard with visualizations
- [ ] Mobile app (React Native)

---

## 🚀 Setup & Running

### Prerequisites

- **Python 3.10+** with `pip`
- **Node.js 18+** with `npm`
- **PostgreSQL 13+** (local or remote)
- `.env` file with required variables

### Environment Setup

Create `.env` file in project root:
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/learnmate_db

# API Keys
CLAUDE_API_KEY=sk-xxx...

# JWT
JWT_SECRET_KEY=your_super_secret_key_change_in_production
JWT_ALGORITHM=HS256

# Server
BACKEND_PORT=8000
FRONTEND_PORT=5173
```

### Backend Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start development server
uvicorn src.backend.main:app --reload

# Run tests
pytest tests/backend/ --cov=src/backend
```

Backend will be available at: **http://localhost:8000**
API docs (Swagger UI): **http://localhost:8000/docs**

### Frontend Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Run tests
npm test

# Run E2E tests
npm run test:e2e
```

Frontend will be available at: **http://localhost:5173**

---

## 📚 Additional Resources

- **Sprint Plan:** [learnmate-sprint-plan.md](planning%20files/learnmate-sprint-plan.md)
- **Project Proposal:** [project3_proposal.md](planning%20files/project3_proposal.md)
- **Development Guide:** [CLAUDE.md](CLAUDE.md)
- **API Documentation:** http://localhost:8000/docs (run backend first)
- **GitHub Repository:** https://github.com/MelanieLLY/LearnMateAI

---

## 🔗 Quick Reference

| Goal | Command |
|------|---------|
| Start backend | `uvicorn src.backend.main:app --reload` |
| Start frontend | `npm run dev` |
| Run all tests | `pytest && npm test` |
| Check types | `npx tsc --noEmit` |
| Lint code | `npm run lint` |
| Format code | `npx prettier --write .` |
| Create migration | `alembic revision --autogenerate -m "<name>"` |
| View test coverage | `pytest --cov=src/backend --cov-report=html` |

---

**Document Version:** 1.0  
**Last Reviewed:** March 28, 2026  
**Status:** Complete and Ready for Review
