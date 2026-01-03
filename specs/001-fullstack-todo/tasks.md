---
description: "Task breakdown for Phase II Full-Stack Todo Web Application"
---

# Tasks: Phase II Full-Stack Todo Web Application

**Input**: Design documents from `/specs/001-fullstack-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md
**Branch**: `001-fullstack-todo`
**Total Tasks**: 67 (Setup: 8, Foundation: 11, US1-US7: 48)

---

## Implementation Strategy

**MVP Scope (Phase 1-3)**: User Registration + Login + Create Task + View Tasks = US1, US2, US3
**Incremental Delivery**: Each user story is independently testable and deployable
**Parallel Execution**: Multiple stories can be worked on simultaneously after foundational phase

**Key Milestones**:
- Phase 1: Project setup (2 days)
- Phase 2: Authentication framework (2 days)
- Phase 3: User Registration (2 days) - **MVP includes up to here**
- Phase 4: User Login (2 days) - **MVP includes up to here**
- Phase 5: Create Task (2 days) - **MVP includes up to here**
- Phase 6: View Tasks (2 days) - **MVP includes up to here**
- Remaining: Update, Delete, Mark Complete (6 days)
- Polish & Deployment (3 days)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and repository structure

- [ ] T001 Clone repository and verify working directory
- [ ] T002 Create backend project structure per plan: `backend/src/models/`, `backend/src/api/`, `backend/tests/`
- [ ] T003 Create frontend project structure per plan: `frontend/src/app/`, `frontend/src/components/`, `frontend/src/hooks/`
- [ ] T004 [P] Initialize backend with `pip` and create `backend/requirements.txt` with FastAPI, SQLModel, PyJWT, Pydantic, psycopg2
- [ ] T005 [P] Initialize frontend with `npm init next-app` and verify TypeScript, Tailwind CSS installation
- [ ] T006 [P] Create `.env.example` files for both backend and frontend with required environment variables
- [ ] T007 Setup `backend/.gitignore` and `frontend/.gitignore` to exclude sensitive files
- [ ] T008 Create `docs/` directory structure with ARCHITECTURE.md, API.md, SETUP.md placeholders

**Checkpoint**: Both backend and frontend projects are scaffolded and ready for dependencies

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Backend Foundation

- [ ] T009 Create `backend/src/config.py` with environment variable loading (DATABASE_URL, JWT_SECRET, ALLOWED_ORIGINS)
- [ ] T010 [P] Create `backend/src/db.py` with Neon PostgreSQL connection pooling using SQLAlchemy
- [ ] T011 [P] Create `backend/src/models/base.py` with SQLModel base class including `id`, `created_at`, `updated_at` fields
- [ ] T012 Implement JWT dependency in `backend/src/api/deps.py` with token verification and user_id extraction
- [ ] T013 [P] Create `backend/src/middleware.py` with CORS middleware configured for frontend origins
- [ ] T014 [P] Create `backend/src/middleware.py` with logging middleware for request/response tracking
- [ ] T015 Create `backend/src/schemas/error.py` with standardized error response schemas (400, 401, 403, 404, 500)
- [ ] T016 Setup `backend/main.py` FastAPI app initialization with middleware stack
- [ ] T017 Create `backend/tests/conftest.py` with pytest fixtures for database session and test client
- [ ] T018 [P] Create `backend/tests/test_health.py` with basic health check endpoint test

### Frontend Foundation

- [ ] T019 Create `frontend/src/types/index.ts` with shared TypeScript types (Task, User, API responses)
- [ ] T020 [P] Create `frontend/src/utils/storage.ts` with JWT token localStorage management
- [ ] T021 [P] Create `frontend/src/services/api.ts` with Fetch wrapper that automatically injects JWT Authorization header
- [ ] T022 Create `frontend/src/hooks/useAuth.ts` custom hook for authentication state management
- [ ] T023 Create `frontend/src/app/layout.tsx` root layout with Tailwind CSS and global styles
- [ ] T024 Create `frontend/src/app/page.tsx` home page that redirects to /login if not authenticated

**Checkpoint**: Authentication framework, API client, database, and middleware are ready - user story implementation can begin

---

## Phase 3: User Story 1 - User Registration (Priority: P1) 🎯 MVP

**Goal**: New users can create accounts with email/password via Better Auth

**Independent Test**: User clicks signup, enters email/password, submits, account is created, user is logged in automatically, JWT is stored, user can access dashboard

### Implementation for User Story 1

#### Backend - User Model & Auth Service

- [ ] T025 [P] [US1] Create `backend/src/models/user.py` SQLModel with id, email, password_hash, created_at (extends base)
- [ ] T026 [US1] Create `backend/src/services/user_service.py` with signup validation (email format, password >= 8 chars)
- [ ] T027 [P] [US1] Create `backend/src/schemas/user.py` with UserCreate schema (email, password validation) and UserResponse schema
- [ ] T028 [P] [US1] Create `backend/src/schemas/auth.py` with SignupRequest and AuthResponse (includes JWT token)

#### Backend - Auth Endpoints

- [ ] T029 [US1] Create `backend/src/api/auth.py` auth routes
- [ ] T030 [US1] Implement `POST /auth/signup` endpoint with: email/password validation, duplicate email check, password hashing, JWT token generation
- [ ] T031 [US1] Add error handling to signup: 400 for invalid email, 409 for duplicate email, 400 for weak password
- [ ] T032 [P] [US1] Update `backend/main.py` to include auth routes

#### Frontend - Signup Page & Better Auth

- [ ] T033 [P] [US1] Install Better Auth SDK: `npm install @better-auth/core @better-auth/next` in frontend
- [ ] T034 [P] [US1] Create `frontend/src/lib/auth.ts` Better Auth client configuration
- [ ] T035 [US1] Create `frontend/src/app/signup/page.tsx` signup form with email/password fields
- [ ] T036 [US1] Implement signup form submission: call Better Auth signup, catch errors, show validation messages
- [ ] T037 [US1] On successful signup: store JWT in localStorage via `storage.ts`, redirect to /dashboard
- [ ] T038 [P] [US1] Create `frontend/src/components/AuthForm.tsx` reusable form component for signup/login
- [ ] T039 [P] [US1] Add Tailwind CSS styling to signup page (responsive, error messages, loading state)

#### Integration - Backend & Frontend

- [ ] T040 [US1] Test signup flow end-to-end: frontend → backend, verify JWT in response, verify stored in localStorage
- [ ] T041 [US1] Verify cross-origin requests work (CORS headers correct)
- [ ] T042 [P] [US1] Add logging to signup endpoints and client calls for debugging

**Checkpoint**: User registration is fully functional. New users can sign up and receive JWT tokens.

---

## Phase 4: User Story 2 - User Login (Priority: P1) 🎯 MVP

**Goal**: Registered users can log in with email/password and receive JWT token

**Independent Test**: User enters credentials on login page, clicks login, receives JWT token, token stored in localStorage, user can access protected routes

### Implementation for User Story 2

#### Backend - Login Endpoint

- [ ] T043 [P] [US2] Create `backend/src/schemas/login.py` with LoginRequest (email, password) and AuthResponse schemas
- [ ] T044 [US2] Implement `POST /auth/login` endpoint in `backend/src/api/auth.py`
- [ ] T045 [US2] Add password verification logic: fetch user by email, compare hashed passwords, return 401 if mismatch
- [ ] T046 [US2] Generate and return JWT token with user_id in payload
- [ ] T047 [P] [US2] Add error handling: 401 for invalid credentials, 404 for user not found

#### Frontend - Login Page

- [ ] T048 [P] [US2] Create `frontend/src/app/login/page.tsx` login form (similar to signup but no password confirmation)
- [ ] T049 [US2] Implement login form submission: call auth service with credentials
- [ ] T050 [US2] On successful login: store JWT in localStorage, redirect to /dashboard
- [ ] T051 [P] [US2] Add "Remember me" and forgot password placeholders (not functional, UI only for Phase II scope)
- [ ] T052 [P] [US2] Style login page with Tailwind CSS

#### Frontend - Auth State Management

- [ ] T053 [US2] Update `frontend/src/hooks/useAuth.ts` to read JWT from localStorage on component mount
- [ ] T054 [US2] Create protected route wrapper component `frontend/src/components/ProtectedRoute.tsx` that checks JWT
- [ ] T055 [US2] Update `frontend/src/app/page.tsx` to redirect to /login if no JWT, else to /dashboard

#### Frontend - Header & Logout

- [ ] T056 [P] [US2] Create `frontend/src/components/Header.tsx` with user email display and logout button
- [ ] T057 [US2] Implement logout: clear JWT from localStorage, redirect to /login
- [ ] T058 [P] [US2] Add Header to `frontend/src/app/layout.tsx` so it appears on all pages

#### Integration

- [ ] T059 [US2] Test complete login flow: login → JWT stored → redirect → header shows email → logout clears JWT
- [ ] T060 [P] [US2] Verify session persistence: refresh page → JWT still valid → user still logged in

**Checkpoint**: User authentication complete. Users can signup, login, logout. JWT tokens are issued and verified. Session persists on page refresh.

---

## Phase 5: User Story 3 - Create Task (Priority: P1) 🎯 MVP

**Goal**: Logged-in users can create new tasks with title and optional description

**Independent Test**: User clicks "Add Task", enters title, submits, task appears immediately in list, refresh page shows task persisted

### Implementation for User Story 3

#### Backend - Task Model & Service

- [ ] T061 [P] [US3] Create `backend/src/models/task.py` SQLModel with id, user_id (FK), title, description, completed, created_at, updated_at
- [ ] T062 [US3] Create `backend/src/services/task_service.py` with task creation, validation (title required, max 200 chars)
- [ ] T063 [P] [US3] Create `backend/src/schemas/task.py` with TaskCreate and TaskResponse schemas
- [ ] T064 [P] [US3] Add database migration or table creation in `backend/src/db.py` for tasks table

#### Backend - Task Creation Endpoint

- [ ] T065 [US3] Create `backend/src/api/tasks.py` routes file
- [ ] T066 [US3] Implement `POST /users/{user_id}/tasks` endpoint: validate JWT, extract user_id, validate title, create task in DB
- [ ] T067 [US3] Add validation: title required (1-200 chars), return 400 if invalid, return 201 with task data
- [ ] T068 [P] [US3] Add error handling: 401 for missing JWT, 403 if user_id in URL doesn't match JWT user_id
- [ ] T069 [P] [US3] Update `backend/main.py` to include tasks routes

#### Frontend - Task Form Component

- [ ] T070 [P] [US3] Create `frontend/src/components/TaskForm.tsx` form with title (required) and description (optional) inputs
- [ ] T071 [P] [US3] Add Tailwind CSS styling to form (modal/inline, validation messages, loading state)
- [ ] T072 [US3] Implement form submission: call API POST /users/{user_id}/tasks with title and description

#### Frontend - Task List & Dashboard

- [ ] T073 [P] [US3] Create `frontend/src/hooks/useTasks.ts` custom hook for task state management and API calls
- [ ] T074 [US3] Create `frontend/src/app/dashboard/page.tsx` main dashboard page
- [ ] T075 [US3] Add TaskForm to dashboard (can be button to open modal or inline form)
- [ ] T076 [P] [US3] Create `frontend/src/components/TaskList.tsx` to display tasks (initially just show title)
- [ ] T077 [US3] Implement task creation in useTasks: optimistic update (add to state immediately), then verify with API
- [ ] T078 [P] [US3] Add "Add Task" button to dashboard

#### Integration

- [ ] T079 [US3] Test task creation flow end-to-end: user logs in → dashboard loads → clicks "Add Task" → form appears → enters title → submits
- [ ] T080 [US3] Verify task appears in list immediately (optimistic), then persists on refresh
- [ ] T081 [P] [US3] Verify error handling: duplicate requests debounced, validation errors shown

**Checkpoint**: Users can create tasks. Tasks are saved to database and displayed on dashboard.

---

## Phase 6: User Story 4 - View Task List (Priority: P1) 🎯 MVP Complete

**Goal**: Users can see all their tasks with completion status displayed

**Independent Test**: User logs in, sees all their tasks, each shows title and completed status, filters (All/Pending/Completed) work

### Implementation for User Story 4

#### Backend - List Tasks Endpoint

- [ ] T082 [P] [US4] Implement `GET /users/{user_id}/tasks` endpoint: extract user_id from JWT, query tasks where user_id matches, return list
- [ ] T083 [US4] Add query parameters: ?completed=true/false for filtering
- [ ] T084 [P] [US4] Add pagination support: ?skip=0&limit=100 (default 100 tasks per page)
- [ ] T085 [P] [US4] Return proper response with list of TaskResponse objects

#### Frontend - Display Task List

- [ ] T086 [P] [US4] Create `frontend/src/components/TaskItem.tsx` component showing task title, completion checkbox, edit/delete buttons
- [ ] T087 [US4] Update TaskList component to call useTasks.getTasks() on mount and display all tasks
- [ ] T088 [P] [US4] Add completed status visual styling (strikethrough, dim color for completed)
- [ ] T089 [P] [US4] Add empty state message: "No tasks yet. Create your first task!"

#### Frontend - Filter Functionality

- [ ] T090 [P] [US4] Create `frontend/src/components/FilterBar.tsx` with "All", "Pending", "Completed" tabs
- [ ] T091 [US4] Update useTasks to support filtering by completed status
- [ ] T092 [P] [US4] Add filter state to dashboard, update task list when filter changes

#### Integration

- [ ] T093 [US4] Test list loading: user logs in → dashboard loads → task list appears with all tasks
- [ ] T094 [US4] Test filtering: click "Pending" → only incomplete tasks shown, click "Completed" → only complete tasks shown
- [ ] T095 [P] [US4] Verify performance: 100 tasks load in < 2 seconds

**Checkpoint**: **MVP COMPLETE**. Users can signup, login, create tasks, and view their task list with filters.

---

## Phase 7: User Story 5 - Update Task (Priority: P2)

**Goal**: Users can edit task title and description

**Independent Test**: User clicks edit on task, changes title, saves, change persists and is visible on refresh

### Implementation for User Story 5

#### Backend - Update Endpoint

- [ ] T096 [P] [US5] Implement `PUT /users/{user_id}/tasks/{task_id}` endpoint: verify user_id matches JWT, update task fields, return 200
- [ ] T097 [US5] Add validation: title required if provided, max 200 chars
- [ ] T098 [P] [US5] Add error handling: 401 unauthorized, 403 forbidden (user_id mismatch), 404 not found
- [ ] T099 [P] [US5] Add updated_at timestamp update

#### Frontend - Edit Task

- [ ] T100 [P] [US5] Create `frontend/src/components/TaskEdit.tsx` modal or inline form for editing
- [ ] T101 [US5] Implement edit button on TaskItem that opens edit form with current task data
- [ ] T102 [P] [US5] Implement form submission: PUT to API, optimistic update, verify persistence
- [ ] T103 [P] [US5] Add cancel button to discard changes

#### Integration

- [ ] T104 [US5] Test edit flow: click edit → form opens with current data → change title → save → verify in list and on refresh

**Checkpoint**: Users can edit tasks. Edit operations are persisted and visible immediately.

---

## Phase 8: User Story 6 - Delete Task (Priority: P2)

**Goal**: Users can permanently remove tasks with confirmation

**Independent Test**: User clicks delete on task, confirms deletion, task removed from list and doesn't reappear on refresh

### Implementation for User Story 6

#### Backend - Delete Endpoint

- [ ] T105 [P] [US6] Implement `DELETE /users/{user_id}/tasks/{task_id}` endpoint: verify user_id, delete task, return 204
- [ ] T106 [US6] Add error handling: 401 unauthorized, 403 forbidden, 404 not found

#### Frontend - Delete Task

- [ ] T107 [P] [US6] Create delete button on TaskItem
- [ ] T108 [US6] Add confirmation dialog: "Are you sure? This cannot be undone."
- [ ] T109 [P] [US6] Implement DELETE call to API, optimistic removal from list
- [ ] T110 [P] [US6] Add error handling: show error message if delete fails

#### Integration

- [ ] T111 [US6] Test delete flow: click delete → confirmation shown → confirm → task removed immediately and on refresh

**Checkpoint**: Users can delete tasks with confirmation dialog.

---

## Phase 9: User Story 7 - Mark Task Complete/Incomplete (Priority: P1)

**Goal**: Users can toggle task completion status with immediate visual feedback

**Independent Test**: User clicks checkbox on task, status changes immediately, refresh page shows status persisted

### Implementation for User Story 7

#### Backend - Mark Complete Endpoint

- [ ] T112 [P] [US7] Implement `PATCH /users/{user_id}/tasks/{task_id}/complete` endpoint: toggle completed status, return 200 with updated task
- [ ] T113 [US7] Add error handling: 401 unauthorized, 403 forbidden, 404 not found

#### Frontend - Completion Toggle

- [ ] T114 [P] [US7] Add checkbox to TaskItem that is checked if task.completed === true
- [ ] T115 [US7] Implement onChange handler: call PATCH endpoint, update state optimistically
- [ ] T116 [P] [US7] Add visual feedback: checkbox state changes immediately, strikethrough appears
- [ ] T117 [P] [US7] Verify persistence: refresh page shows completed status

#### Integration

- [ ] T118 [US7] Test completion flow: click checkbox → changes immediately → filter to "Completed" → task appears → refresh → status persists

**Checkpoint**: All core task operations complete. Users can create, read, update, delete, and mark tasks complete.

---

## Phase 10: Polish & Cross-Cutting Concerns

### Error Handling & Validation

- [ ] T119 [P] Add input sanitization for title and description on frontend and backend
- [ ] T120 Add network error handling: show retry button if API calls fail
- [ ] T121 [P] Add duplicate request prevention: debounce rapid submissions

### Testing

- [ ] T122 [P] Write backend pytest tests for all endpoints in `backend/tests/test_auth.py` and `backend/tests/test_tasks.py`
- [ ] T123 Add frontend integration tests in `frontend/tests/integration/` using Jest
- [ ] T124 [P] Manual end-to-end testing: complete user journey signup → login → create → view → edit → complete → delete

### Documentation

- [ ] T125 Write `docs/ARCHITECTURE.md` with system design diagrams
- [ ] T126 Write `docs/API.md` with detailed endpoint documentation
- [ ] T127 [P] Write `docs/SETUP.md` with development environment setup instructions
- [ ] T128 Write `docs/DEPLOYMENT.md` with Vercel and Cloud Run deployment steps

### Performance & Optimization

- [ ] T129 Optimize frontend bundle: check bundle size, enable code splitting
- [ ] T130 [P] Add caching headers to API responses
- [ ] T131 Add database indexes on user_id and created_at fields

### Security Review

- [ ] T132 [P] Review CORS configuration: ensure only trusted origins allowed
- [ ] T133 Verify JWT secret is secure and never committed to git
- [ ] T134 [P] Test SQL injection prevention: validate input sanitization
- [ ] T135 Test XSS prevention: verify HTML is escaped in frontend

### Deployment Preparation

- [ ] T136 Setup GitHub Actions CI/CD pipeline (or equivalent)
- [ ] T137 [P] Create deployment script for backend to Cloud Run
- [ ] T138 Configure Vercel deployment for frontend
- [ ] T139 [P] Setup environment variables on Vercel and Cloud Run
- [ ] T140 Create production `.env` file for Neon PostgreSQL connection

---

## Task Organization Summary

### By User Story (Feature Priorities)

| Story | Title | Priority | Tasks | MVP? |
|-------|-------|----------|-------|------|
| US1 | User Registration | P1 | T025-T042 (18) | ✅ Yes |
| US2 | User Login | P1 | T043-T060 (18) | ✅ Yes |
| US3 | Create Task | P1 | T061-T081 (21) | ✅ Yes |
| US4 | View Tasks | P1 | T082-T095 (14) | ✅ Yes |
| US5 | Update Task | P2 | T096-T104 (9) | No |
| US6 | Delete Task | P2 | T105-T111 (7) | No |
| US7 | Mark Complete | P1 | T112-T118 (7) | ✅ Yes |
| - | Foundation | - | T009-T024 (16) | ✅ Yes |
| - | Setup | - | T001-T008 (8) | ✅ Yes |
| - | Polish | - | T119-T140 (22) | No |

### Parallel Execution Opportunities

**After Phase 2 (Foundation) completes, these can run in parallel**:

| Task Group | Parallelizable Tasks | Dependencies |
|------------|---------------------|--------------|
| US1 Backend | T025-T032 (auth model, endpoints) | Foundation complete (Phase 2) |
| US1 Frontend | T033-T039 (signup, Better Auth) | T023 (useAuth hook) |
| US2 Backend | T043-T047 (login endpoint) | T025 (User model) |
| US2 Frontend | T048-T058 (login, header, logout) | T033 (Better Auth setup) |
| US3 Backend | T061-T069 (task model, endpoint) | Foundation complete |
| US3 Frontend | T070-T081 (form, list, dashboard) | T023, T024 (hooks, layout) |
| US4 Backend | T082-T085 (list endpoint) | T061 (Task model) |
| US4 Frontend | T086-T095 (display, filters) | T074 (dashboard page) |

**Optimal 2-person team division**:
- Developer 1: Backend (FastAPI, SQLModel, authentication, endpoints)
- Developer 2: Frontend (Next.js, Better Auth, components, UI)
- Both contribute to integration testing

---

## MVP Scope & Delivery

**Minimum Viable Product (MVP)** includes:
- Phase 1: Setup (T001-T008)
- Phase 2: Foundation (T009-T024)
- Phase 3: User Registration (T025-T042)
- Phase 4: User Login (T043-T060)
- Phase 5: Create Task (T061-T081)
- Phase 6: View Tasks (T082-T095)
- Phase 9: Mark Complete (T112-T118)

**MVP Total**: 8 + 16 + 18 + 18 + 21 + 14 + 7 = **102 implementation tasks**

**Non-MVP features** (Phase 7-8): Update Task, Delete Task

**Post-MVP** (Phase 10): Testing, documentation, optimization, deployment

---

## Dependencies Graph

```
Phase 1: Setup
  ↓
Phase 2: Foundation (GATE - nothing starts until complete)
  ├→ Phase 3: US1 (Registration)
  │   ├→ Phase 4: US2 (Login) [depends on US1]
  │   └→ Phase 5: US3 (Create Task) [independent]
  │       ├→ Phase 6: US4 (View Tasks)
  │       ├→ Phase 7: US5 (Update Task)
  │       └→ Phase 8: US6 (Delete Task)
  └→ Phase 9: US7 (Mark Complete) [independent of US5-US6]
↓
Phase 10: Polish, Testing, Deployment
```

**Sequential path (3-person team)**:
1. All: Phase 1 Setup (1 day)
2. All: Phase 2 Foundation (1 day)
3. Dev1+Dev2: Phase 3 (US1) in parallel - 2 days
4. Dev1+Dev2: Phase 4 (US2) in parallel - 2 days
5. Dev1+Dev2+Dev3: Phase 5 (US3), Phase 7 (US5), Phase 9 (US7) in parallel - 3 days
6. Dev1+Dev2+Dev3: Phase 6 (US4), Phase 8 (US6) - 2 days
7. All: Phase 10 Polish - 2 days

**Total: ~15 days for full feature**

---

## Next Steps

1. ✅ Specification complete (spec.md)
2. ✅ Implementation plan complete (plan.md)
3. ✅ Task breakdown complete (tasks.md - this file)
4. ⏭️ Begin Phase 1: Setup (create project structure)
5. ⏭️ Begin Phase 2: Foundation (database, auth middleware)
6. ⏭️ Begin Phase 3+: User stories in priority order

---

## Document Versioning

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-03 | Initial task breakdown - 140 tasks across 10 phases |
