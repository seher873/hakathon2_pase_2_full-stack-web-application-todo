---
description: "Task breakdown for AI Skills Layer for Todo Application"
---

# Tasks: AI Skills Layer for Todo Application

**Input**: Design documents from `/specs/001-fullstack-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md
**Branch**: `ai-skills-preview`
**Total Tasks**: 35 (Setup: 5, Foundation: 8, US1-US3: 18, Polish: 4)

---

## Implementation Strategy

**MVP Scope (Phase 1-3)**: AI Skills Module Setup + Intent Detection + Basic Skill Execution = All 3 skills operational
**Incremental Delivery**: Each skill is tested individually before integration
**Parallel Execution**: Skills can be developed in parallel after foundational phase

**Key Milestones**:
- Phase 1: Project setup and structure (1 day)
- Phase 2: Foundation and security (1 day)
- Phase 3: Intent detection and routing (1 day) - **MVP includes up to here**
- Phase 4: create_task skill implementation (1 day) - **MVP includes up to here**
- Phase 5: list_tasks skill implementation (1 day) - **MVP includes up to here**
- Phase 6: complete_task skill implementation (1 day) - **MVP includes up to here**
- Remaining: Polish, testing, documentation (2 days)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and skills module structure

- [X] T001 Create backend/skills directory structure per plan: `__init__.py`, `todo_skills.py`, `api.py`, `README.md`, `example.py`
- [X] T002 [P] Create AI skills specification file at specs/ai/skills.md with all supported skills and constraints
- [X] T003 [P] Define skill-to-API mapping in documentation: create_task → POST /tasks, list_tasks → GET /tasks, complete_task → PATCH /tasks/{id}/complete
- [X] T004 Create backend/skills/__init__.py to initialize skills module
- [X] T005 Setup backend/skills/README.md with usage instructions and clear Phase-3 Preview labeling

**Checkpoint**: Skills module structure is created and documented

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY skill implementation

**⚠️ CRITICAL**: No skill work can begin until this phase is complete

### Skills Foundation

- [X] T006 Create backend/skills/todo_skills.py with basic TodoSkills class structure
- [X] T007 [P] Implement JWT token forwarding mechanism in TodoSkills to maintain user isolation
- [X] T008 [P] Create request/response utilities in todo_skills.py for API calls to existing endpoints
- [X] T009 Implement security validation: ensure JWT is required and user isolation is enforced
- [X] T010 Create basic skill executor interface in todo_skills.py
- [X] T011 [P] Add error handling and response formatting utilities to maintain API consistency
- [X] T012 [P] Update backend/main.py to include AI skills routes: /api/ai/process and /api/ai/skills
- [X] T013 Create basic tests in backend/tests/test_skills.py for foundation components

**Checkpoint**: Skills foundation is complete - skill implementation can begin

---

## Phase 3: Intent Detection & Routing (Priority: P1) 🎯 MVP

**Goal**: Process natural language input and route to appropriate skill

**Independent Test**: User sends "Add buy milk", system detects create_task intent, routes to create_task skill

### Implementation for Intent Detection

#### Pattern Matching & Detection
- [X] T014 [P] [US1] Implement pattern matching for create_task intents: "Add", "Create task", "New task", etc.
- [X] T015 [US1] Implement pattern matching for list_tasks intents: "Show my tasks", "List my tasks", etc.
- [X] T016 [P] [US1] Implement pattern matching for complete_task intents: "Complete", "Finish", "Mark done", etc.
- [X] T017 [US1] Create intent detection function that maps user input to skill names
- [X] T018 [P] [US1] Add fallback handling for unrecognized intents with clear error messages

#### Skill Routing
- [X] T019 [US1] Create skill router that maps detected intent to skill function
- [X] T020 [P] [US1] Implement process_request function that orchestrates intent detection → routing → execution
- [X] T021 [US1] Add logging for intent detection and routing decisions
- [X] T022 [P] [US1] Test intent detection with sample inputs from spec

**Checkpoint**: Natural language processing works - inputs are correctly routed to appropriate skills.

---

## Phase 4: create_task Skill (Priority: P1) 🎯 MVP

**Goal**: Process natural language to create new tasks via existing API

**Independent Test**: User says "Add buy milk", system creates task via POST /users/{id}/tasks API call

### Implementation for create_task Skill

#### Skill Implementation
- [X] T023 [P] [US2] Create create_task function in todo_skills.py that accepts user_id, title, description, jwt_token
- [X] T024 [US2] Implement parsing of task title and description from natural language input
- [X] T025 [P] [US2] Add API call to existing POST /users/{user_id}/tasks endpoint with proper JWT token
- [X] T026 [US2] Handle API response and format for AI response consistency
- [X] T027 [P] [US2] Add validation: ensure title is extracted from input, handle missing descriptions gracefully

#### Integration
- [X] T028 [US2] Integrate create_task skill with intent detector and router
- [X] T029 [P] [US2] Test complete flow: "Add buy milk" → intent detection → create_task execution → API call
- [X] T030 [US2] Verify error handling: invalid inputs, API failures, authentication issues

**Checkpoint**: create_task skill works end-to-end - natural language creates tasks via existing API.

---

## Phase 5: list_tasks Skill (Priority: P1) 🎯 MVP

**Goal**: Process natural language to list user's tasks via existing API

**Independent Test**: User says "Show my tasks", system retrieves tasks via GET /users/{id}/tasks API call

### Implementation for list_tasks Skill

#### Skill Implementation
- [X] T031 [P] [US3] Create list_tasks function in todo_skills.py that accepts user_id and jwt_token
- [ ] T032 [US3] Add API call to existing GET /users/{user_id}/tasks endpoint with proper JWT token
- [ ] T033 [P] [US3] Handle API response and format for AI response consistency
- [ ] T034 [US3] Implement response formatting to show task count and basic information

#### Integration
- [ ] T035 [US3] Integrate list_tasks skill with intent detector and router
- [ ] T036 [P] [US3] Test complete flow: "Show my tasks" → intent detection → list_tasks execution → API call
- [ ] T037 [US3] Verify error handling: API failures, authentication issues

**Checkpoint**: list_tasks skill works end-to-end - natural language retrieves tasks via existing API.

---

## Phase 6: complete_task Skill (Priority: P1) 🎯 MVP Complete

**Goal**: Process natural language to mark tasks complete via existing API

**Independent Test**: User says "Complete buy milk", system finds and marks task via PATCH /users/{id}/tasks/{id}/complete API call

### Implementation for complete_task Skill

#### Skill Implementation
- [ ] T038 [P] [US4] Create complete_task function in todo_skills.py that accepts user_id, task identifier, completed status, jwt_token
- [ ] T039 [US4] Implement logic to identify specific task from natural language (by title matching)
- [ ] T040 [P] [US4] Add API call to existing GET /users/{user_id}/tasks to find matching task
- [ ] T041 [US4] Add API call to existing PATCH /users/{user_id}/tasks/{task_id}/complete endpoint with proper JWT token
- [ ] T042 [P] [US4] Handle API response and format for AI response consistency

#### Integration
- [ ] T043 [US4] Integrate complete_task skill with intent detector and router
- [ ] T044 [P] [US4] Test complete flow: "Complete buy milk" → intent detection → complete_task execution → API calls
- [ ] T045 [US4] Verify error handling: task not found, API failures, authentication issues

**Checkpoint**: **MVP COMPLETE**. All 3 skills work - users can create, list, and complete tasks via natural language.

---

## Phase 7: API Endpoints & Integration

**Goal**: Expose AI skills through proper API endpoints

### API Implementation
- [ ] T046 [P] Create POST /api/ai/process endpoint in backend/skills/api.py
- [ ] T047 Create GET /api/ai/skills endpoint to list available skills with examples
- [ ] T048 [P] Add proper request validation for AI input (ensure non-empty, length limits)
- [ ] T049 Add proper response formatting following existing SuccessResponse pattern
- [ ] T050 [P] Implement error handling for API endpoints with consistent error responses

### Integration Testing
- [ ] T051 Test all AI endpoints with proper JWT authentication
- [ ] T052 [P] Verify user isolation: users can only access their own data through AI skills
- [ ] T053 Test error scenarios: invalid JWT, malformed requests, API failures

**Checkpoint**: AI skills are accessible via proper API endpoints with security validation.

---

## Phase 8: Polish & Cross-Cutting Concerns

### Testing & Validation
- [ ] T054 [P] Write comprehensive unit tests for all skill functions
- [ ] T055 Add integration tests for complete AI skill flows
- [ ] T056 [P] Test security: verify JWT tokens are properly validated and user isolation is maintained

### Documentation & Examples
- [ ] T057 Update backend/skills/README.md with clear Phase-3 Preview labeling and no impact on Phase-2 grading
- [ ] T058 [P] Create backend/skills/example.py demonstrating all 3 skills with example usage
- [ ] T059 Add inline documentation to all skill functions explaining inputs, outputs, and constraints
- [ ] T060 [P] Update API documentation with new AI endpoints and usage examples

**Checkpoint**: AI skills are fully tested, documented, and clearly labeled as Phase-3 Preview.

---

## Task Organization Summary

### By User Story (Skill Priorities)

| Story | Title | Priority | Tasks | MVP? |
|-------|-------|----------|-------|------|
| US1 | Intent Detection | P1 | T014-T022 (9) | ✅ Yes |
| US2 | create_task Skill | P1 | T023-T030 (8) | ✅ Yes |
| US3 | list_tasks Skill | P1 | T031-T037 (7) | ✅ Yes |
| US4 | complete_task Skill | P1 | T038-T045 (8) | ✅ Yes |
| - | Foundation | - | T006-T013 (8) | ✅ Yes |
| - | Setup | - | T001-T005 (5) | ✅ Yes |
| - | API & Integration | - | T046-T053 (8) | ✅ Yes |
| - | Polish | - | T054-T060 (7) | No |

### Parallel Execution Opportunities

**After Phase 2 (Foundation) completes, these can run in parallel**:

| Task Group | Parallelizable Tasks | Dependencies |
|------------|---------------------|--------------|
| US1 Skills | T014-T022 (intent detection) | Foundation complete (Phase 2) |
| US2 Skills | T023-T030 (create_task) | T019 (routing function) |
| US3 Skills | T031-T037 (list_tasks) | T019 (routing function) |
| US4 Skills | T038-T045 (complete_task) | T019 (routing function), T031 (list_tasks for task lookup) |

**Optimal 2-person team division**:
- Developer 1: Intent detection and routing (US1), create_task skill (US2)
- Developer 2: list_tasks skill (US3), complete_task skill (US4)
- Both contribute to API integration and testing

---

## MVP Scope & Delivery

**Minimum Viable Product (MVP)** includes:
- Phase 1: Setup (T001-T005)
- Phase 2: Foundation (T006-T013)
- Phase 3: Intent Detection (T014-T022)
- Phase 4: create_task Skill (T023-T030)
- Phase 5: list_tasks Skill (T031-T037)
- Phase 6: complete_task Skill (T038-T045)

**MVP Total**: 5 + 8 + 9 + 8 + 7 + 8 = **45 implementation tasks**

**Non-MVP features** (Phase 7-8): API endpoints, comprehensive testing, documentation

**Post-MVP** (Phase 8): Testing, documentation, polish

---

## Dependencies Graph

```
Phase 1: Setup
  ↓
Phase 2: Foundation (GATE - nothing starts until complete)
  ├→ Phase 3: Intent Detection & Routing
  │   ├→ Phase 4: create_task Skill
  │   ├→ Phase 5: list_tasks Skill
  │   └→ Phase 6: complete_task Skill
  ├→ Phase 7: API Endpoints & Integration (after Phase 4-6 complete)
  └→ Phase 8: Polish & Documentation (after all skills complete)
```

**Sequential path (2-person team)**:
1. Both: Phase 1 Setup (0.5 day)
2. Both: Phase 2 Foundation (0.5 day)
3. Dev1: Phase 3 Intent Detection (1 day)
4. Dev1: Phase 4 create_task Skill (1 day)
5. Dev2: Phase 5 list_tasks Skill (1 day)
6. Dev1+Dev2: Phase 6 complete_task Skill (1 day)
7. Both: Phase 7 API Integration (0.5 day)
8. Both: Phase 8 Polish (0.5 day)

**Total: ~6 days for full feature**

---

## Next Steps

1. ✅ Specification complete (spec.md)
2. ✅ Implementation plan complete (plan.md)
3. ✅ Task breakdown complete (tasks.md - this file)
4. ⏭️ Begin Phase 1: Setup (create skills module structure)
5. ⏭️ Begin Phase 2: Foundation (security and core infrastructure)
6. ⏭️ Begin Phase 3+: Skills implementation in priority order
7. ⏭️ Complete Phase 7-8: Integration and polish

---

## Document Versioning

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-09 | Initial task breakdown - 60 tasks across 8 phases |