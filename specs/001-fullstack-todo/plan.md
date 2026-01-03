# Implementation Plan: Phase II Full-Stack Todo Web Application

**Branch**: `001-fullstack-todo` | **Date**: 2026-01-03 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-fullstack-todo/spec.md`

## Summary

Transform Phase I console todo app into a production-ready multi-user web application with secure JWT authentication, user-isolated REST API, and responsive Next.js frontend backed by Neon PostgreSQL. Delivers core CRUD operations (create, read, update, delete, mark-complete) with strict user isolation at database and API layers.

## Technical Context

**Frontend Language/Version**: TypeScript with Next.js 16+ (App Router)
**Backend Language/Version**: Python 3.10+
**Primary Frontend Dependencies**: Next.js, React 18+, Tailwind CSS, Better Auth SDK, Fetch API
**Primary Backend Dependencies**: FastAPI, SQLModel, PyJWT, Pydantic, psycopg2/asyncpg
**Storage**: Neon Serverless PostgreSQL (managed)
**Testing**: pytest (backend), Jest + React Testing Library (frontend)
**Target Platform**: Web (Vercel frontend + Cloud Run/Vercel Functions backend)
**Project Type**: Web application (monorepo with frontend + backend)
**Performance Goals**: Task operations < 500ms; list load < 2s; API response < 200ms; support 1000+ concurrent users
**Constraints**: Stateless API, strict user isolation, JWT-only authentication, environment-based secrets
**Scale/Scope**: Multi-user (100+ users), 1000s tasks, real-time updates via polling/optimistic UI

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Spec-Driven Development (SDD)
✅ **PASS** - Feature specification complete with 7 user stories, 15 functional requirements, 10 success criteria. All work driven from spec requirements.

### Principle II: Explicit Planning & Architecture
✅ **PASS** - This plan documents all architectural decisions (REST API, JWT, SQLModel, Neon). All significant decisions will have ADRs if they impact system design.

### Principle III: Test-Driven Development (TDD)
✅ **PASS** - Backend will use pytest with fixtures for JWT testing. Frontend will use Jest + React Testing Library. All acceptance scenarios from spec will have corresponding tests.

### Principle IV: Small, Testable Changes
✅ **PASS** - Implementation will follow task-based breakdown. Each task is independently testable and references spec requirements.

### Principle V: Observable, Debuggable Systems
✅ **PASS** - Backend will log all requests, authentication, and database operations. Frontend will expose user state and API calls for debugging. Error responses include structured error messages.

**GATE RESULT**: ✅ **PASS** - All constitutional principles satisfied. Proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

**SELECTED: Option 2 - Web Application Monorepo**

```text
hackathon-todo/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Environment template
│   ├── src/
│   │   ├── models/             # SQLModel ORM models
│   │   │   ├── task.py         # Task model definition
│   │   │   └── user.py         # User model (Better Auth managed)
│   │   ├── api/                # API routes
│   │   │   ├── auth.py         # Auth endpoints (login/signup)
│   │   │   ├── tasks.py        # Task CRUD endpoints
│   │   │   └── deps.py         # Dependencies (JWT verification)
│   │   ├── db.py               # Database connection (Neon)
│   │   ├── config.py           # Configuration (env vars)
│   │   └── middleware.py       # CORS, logging middleware
│   └── tests/
│       ├── conftest.py         # pytest fixtures
│       ├── test_auth.py        # Authentication tests
│       ├── test_tasks.py       # Task CRUD tests
│       └── test_integration.py # Full flow integration tests
│
├── frontend/
│   ├── package.json            # Node dependencies
│   ├── .env.example            # Environment template
│   ├── tsconfig.json           # TypeScript configuration
│   ├── tailwind.config.js      # Tailwind CSS config
│   ├── next.config.js          # Next.js configuration
│   ├── src/
│   │   ├── app/                # Next.js App Router
│   │   │   ├── layout.tsx      # Root layout
│   │   │   ├── page.tsx        # Home page (redirect to dashboard)
│   │   │   ├── login/          # Login page
│   │   │   ├── signup/         # Signup page
│   │   │   └── dashboard/      # Protected dashboard
│   │   ├── components/         # Reusable components
│   │   │   ├── TaskForm.tsx    # Add/edit task form
│   │   │   ├── TaskList.tsx    # Task list display
│   │   │   ├── TaskItem.tsx    # Individual task item
│   │   │   └── Header.tsx      # Navigation header
│   │   ├── hooks/              # Custom React hooks
│   │   │   ├── useAuth.ts      # Authentication hook
│   │   │   └── useTasks.ts     # Task management hook
│   │   ├── services/           # API client layer
│   │   │   └── api.ts          # Fetch wrapper with JWT injection
│   │   ├── types/              # TypeScript types
│   │   │   └── index.ts        # Shared type definitions
│   │   └── utils/              # Utility functions
│   │       └── storage.ts      # localStorage JWT management
│   └── tests/
│       ├── __mocks__/          # Mock data and handlers
│       ├── components/         # Component tests
│       └── integration/        # E2E style tests
│
├── docs/                       # Documentation
│   ├── ARCHITECTURE.md         # System design
│   ├── API.md                  # API specification
│   ├── SETUP.md                # Setup instructions
│   └── DEPLOYMENT.md           # Deployment guide
│
├── .spec-kit/
│   └── config.yaml             # Spec-Kit configuration
│
├── specs/
│   └── 001-fullstack-todo/     # This feature specs
│       ├── spec.md             # Feature specification
│       ├── plan.md             # This file
│       ├── research.md         # Phase 0 research findings
│       ├── data-model.md       # Phase 1 data model design
│       ├── quickstart.md       # Phase 1 setup guide
│       ├── contracts/          # Phase 1 API contracts
│       └── tasks.md            # Phase 2 task breakdown
│
├── CLAUDE.md                   # Root development rules
├── README.md                   # Project overview
└── .env.example                # Root environment template
```

**Structure Decision**: Web application monorepo with separate backend (FastAPI/Python) and frontend (Next.js/TypeScript) directories. Shared documentation in `docs/` and `specs/`. Each service has its own dependencies, configuration, and tests. This structure supports independent deployment while maintaining a unified feature specification.

## Phase 0: Research & Clarifications

**Status**: Ready for execution

### Research Tasks
1. **Better Auth Integration Pattern** - How to integrate Better Auth SDK in Next.js App Router for user management
2. **JWT Verification in FastAPI** - Best practices for JWT middleware in FastAPI with user context extraction
3. **Neon Connection Pooling** - Optimal connection string configuration for serverless PostgreSQL
4. **SQLModel Type Safety** - Patterns for SQLModel schema with Pydantic validation
5. **CORS Configuration** - Vercel frontend to Cloud Run backend CORS setup

### Decisions Made (No Clarifications Needed)
- ✅ Authentication method: JWT (issued by Better Auth, verified by backend)
- ✅ Database: Neon Serverless PostgreSQL
- ✅ ORM: SQLModel (combines SQLAlchemy + Pydantic)
- ✅ API Style: RESTful JSON with standard HTTP status codes
- ✅ Data isolation: User ID from JWT token verified on all queries

---

## Phase 1: Design & Contracts

### 1.1 Data Model Design

**Entities**:

**User** (Managed by Better Auth)
- `id`: UUID (primary key)
- `email`: String (unique)
- `password`: String (hashed by Better Auth)
- `created_at`: Timestamp
- `updated_at`: Timestamp

**Task** (SQLModel)
- `id`: UUID (primary key)
- `user_id`: UUID (foreign key → User.id)
- `title`: String (1-200 characters, required)
- `description`: String (optional, unlimited length)
- `completed`: Boolean (default: False)
- `created_at`: Timestamp
- `updated_at`: Timestamp

**Relationships**:
- One User has many Tasks (1:N)
- One Task belongs to one User (N:1)
- All task queries filtered by `user_id` from JWT

**Validation Rules**:
- Task title is required and non-empty
- Task title max 200 characters
- Description optional, no max length
- Completed is boolean (true/false)
- User can only access/modify their own tasks

### 1.2 API Contracts

**Base URL**: `https://api.example.com/api`

**Authentication**: All endpoints (except signup/login) require:
```
Authorization: Bearer {jwt_token}
```

**Endpoints**:

#### Authentication (No JWT Required)
- `POST /auth/signup` - Create new user account
- `POST /auth/login` - Authenticate user (via Better Auth)

#### Tasks (JWT Required)
- `GET /users/{user_id}/tasks` - List all user's tasks
- `POST /users/{user_id}/tasks` - Create new task
- `GET /users/{user_id}/tasks/{task_id}` - Get single task details
- `PUT /users/{user_id}/tasks/{task_id}` - Update task (title/description)
- `DELETE /users/{user_id}/tasks/{task_id}` - Delete task
- `PATCH /users/{user_id}/tasks/{task_id}/complete` - Toggle completion

**Status Codes**:
- 200 OK - Successful GET, PUT, PATCH
- 201 Created - Successful POST
- 204 No Content - Successful DELETE
- 400 Bad Request - Invalid input
- 401 Unauthorized - Missing/invalid JWT
- 403 Forbidden - User accessing another user's task
- 404 Not Found - Task doesn't exist
- 500 Internal Server Error - Server error

**Response Format** (Success):
```json
{
  "status": "success",
  "data": { /* entity or list */ },
  "timestamp": "2026-01-03T12:00:00Z"
}
```

**Response Format** (Error):
```json
{
  "status": "error",
  "code": "INVALID_REQUEST",
  "message": "Human-readable error message",
  "details": { /* optional validation details */ },
  "timestamp": "2026-01-03T12:00:00Z"
}
```

### 1.3 Frontend Architecture

**Page Structure**:
- `/` - Root (redirects to /login if not authenticated)
- `/login` - Login page (email/password form)
- `/signup` - Signup page (email/password form)
- `/dashboard` - Protected task list and management (requires auth)

**Component Hierarchy**:
```
App (layout.tsx)
├── Header (navigation, logout)
├── Routes
│   ├── LoginPage
│   ├── SignupPage
│   └── DashboardPage
│       ├── TaskForm (add/edit)
│       ├── FilterBar (All/Pending/Completed)
│       └── TaskList
│           └── TaskItem (with checkbox, edit, delete)
```

**State Management**:
- Authentication: Custom `useAuth` hook (JWT in localStorage)
- Tasks: Custom `useTasks` hook (API client with JWT injection)
- UI State: React hooks (loading, filters, form state)

### 1.4 Backend Architecture

**Directory Structure**:
- `main.py` - FastAPI app initialization, middleware, routes
- `config.py` - Environment configuration (DATABASE_URL, JWT_SECRET)
- `db.py` - Neon database connection and session management
- `models/` - SQLModel entity definitions
- `api/` - Route handlers with JWT verification
- `middleware.py` - CORS, logging, error handling

**Middleware Stack**:
1. CORS middleware (allow frontend origin)
2. Logging middleware (track requests/responses)
3. JWT verification middleware (extract user_id)
4. Error handling middleware (consistent error responses)

---

## Phase 2: Task Breakdown

**Output**: `tasks.md` (generated by `/sp.tasks` command)

Tasks will be grouped by priority (P1 features first) and dependencies:

**P1 - Core Infrastructure**:
- Backend: Setup FastAPI project, Neon connection, SQLModel models
- Frontend: Setup Next.js project, Better Auth integration
- Auth: Implement JWT verification middleware

**P1 - Authentication**:
- Backend: Auth endpoints (signup/login)
- Frontend: Login/Signup pages with Better Auth
- Integration: JWT token exchange and storage

**P1 - Task CRUD**:
- Backend: Task model and database operations
- Backend: CRUD endpoints with user isolation
- Frontend: Task creation, viewing, deletion
- Frontend: Mark complete/incomplete

**P2 - Polish & Testing**:
- Error handling and validation
- Integration tests
- Performance optimization
- Documentation

---

## Design Decision Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Frontend Framework | Next.js 16+ App Router | Modern, SSR support, Vercel native |
| Backend Framework | FastAPI | High performance, async support, built-in validation |
| ORM | SQLModel | Type-safe, Pydantic integration, SQLAlchemy power |
| Database | Neon PostgreSQL | Serverless, auto-scaling, Vercel integration |
| Auth | Better Auth + JWT | Managed OAuth, simple JWT for API |
| API Style | REST/JSON | Simple, cacheable, standard HTTP semantics |
| UI Framework | Tailwind CSS | Utility-first, responsive, zero runtime |
| Testing | pytest + Jest | Industry standard, comprehensive coverage |

---

## Architectural Decision Records (ADRs)

The following decisions meet significance criteria and will require ADRs:

1. **ADR-001**: JWT-based stateless authentication (impact: security, scalability)
2. **ADR-002**: Monorepo structure vs. separate repositories (impact: deployment, CI/CD)
3. **ADR-003**: SQLModel choice over Tortoise ORM (impact: type safety, migration path)

ADRs will be created during implementation when decisions are finalized.

---

## Implementation Phases Summary

| Phase | Deliverables | Duration |
|-------|--------------|----------|
| **Phase 0** | research.md with all decisions | Parallel with Phase 1 |
| **Phase 1** | data-model.md, API contracts, quickstart.md | Design complete |
| **Phase 2** | tasks.md with task breakdown | Approx 40-50 tasks |
| **Phase 3+** | Implementation per tasks.md | Iterative development |

---

## Next Steps

1. ✅ Specification complete (`spec.md`)
2. ✅ Implementation plan complete (`plan.md` - this file)
3. ⏭️ Run `/sp.tasks` to generate task breakdown
4. ⏭️ Begin implementation following task list
5. ⏭️ Each completed task updates corresponding tests

---

## Document Versioning

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-03 | Initial implementation plan |
