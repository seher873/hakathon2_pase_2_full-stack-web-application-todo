# Implementation Plan: AI Skills Layer for Todo Application

**Branch**: `ai-skills-preview` | **Date**: 2026-01-09 | **Spec**: [Feature Spec]
**Input**: AI Skills Preview specification for Phase 3

## Summary

Implement an AI Skills layer that sits between user chat input and existing Phase-2 backend APIs. The system will process natural language requests, detect intent, route to appropriate skills, and execute existing REST API calls while maintaining security and authentication.

## Technical Context

**Frontend Language/Version**: N/A (Backend service)
**Backend Language/Version**: Python 3.10+
**Primary Dependencies**: FastAPI, Pydantic, SQLAlchemy/SQLModel, requests
**AI Integration**: Natural language processing with pattern matching
**Target Platform**: Backend service integrated with existing API
**Performance Goals**: <500ms response time for intent detection and skill execution
**Constraints**: Must use existing Phase-2 APIs, maintain JWT authentication, ensure user isolation
**Scale/Scope**: Support concurrent users, handle natural language processing efficiently

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Spec-Driven Development (SDD)
✅ **PASS** - Feature specification complete with architecture, components, and flow defined. All work driven from spec requirements.

### Principle II: Explicit Planning & Architecture
✅ **PASS** - This plan documents all architectural decisions (AI layer between chat and APIs, intent detection, skill routing). All significant decisions will have ADRs if they impact system design.

### Principle III: Test-Driven Development (TDD)
✅ **PASS** - Backend will use pytest with fixtures for JWT testing. All acceptance scenarios from spec will have corresponding tests.

### Principle IV: Small, Testable Changes
✅ **PASS** - Implementation will follow task-based breakdown. Each component is independently testable and references spec requirements.

### Principle V: Observable, Debuggable Systems
✅ **PASS** - Backend will log all AI requests, intent detection, and skill execution. Error responses include structured error messages.

**GATE RESULT**: ✅ **PASS** - All constitutional principles satisfied. Proceed to Phase 0.

## Project Structure

### Implementation (this feature)

```text
backend/skills/
├── __init__.py              # Skills module initialization
├── todo_skills.py           # Core skill implementations
├── api.py                   # AI skills API endpoints
├── README.md               # Skills documentation
└── example.py              # Usage examples
```

## Phase 0: Research & Clarifications

**Status**: Ready for execution

### Research Tasks
1. **Natural Language Processing Pattern Matching** - Best practices for mapping user intents to skills using regex patterns
2. **JWT Token Forwarding** - Secure patterns for passing JWT tokens between AI layer and existing APIs
3. **Intent Detection Algorithms** - Simple and effective intent detection without complex ML models
4. **API Integration Patterns** - Best practices for calling existing REST APIs from AI layer
5. **Security Considerations** - Ensuring user isolation and authentication flow remains intact

### Decisions Made (No Clarifications Needed)
- ✅ Intent detection method: Pattern matching with regex (simple and effective)
- ✅ Token handling: Forward JWT tokens unchanged to existing APIs
- ✅ Skill routing: Direct mapping from detected intent to skill functions
- ✅ API integration: HTTP requests to existing Phase-2 endpoints
- ✅ Data isolation: Rely on existing JWT-based user isolation in backend

---
## Phase 1: Design & Contracts

### 1.1 Data Model Design

**No new data models needed** - Skills layer uses existing Phase-2 models through API calls.

### 1.2 API Contracts

**Base URL**: `https://api.example.com/api`

**Authentication**: All AI endpoints require:
```
Authorization: Bearer {jwt_token}
```

**Endpoints**:

#### AI Skills (JWT Required)
- `POST /ai/process` - Process natural language request and execute appropriate skill
- `GET /ai/skills` - Get list of available skills and examples

**Request Format** (`POST /ai/process`):
```json
{
  "input": "Natural language request (e.g., 'Add buy milk')"
}
```

**Response Format** (Success):
```json
{
  "status": "success",
  "data": {
    "skill": "create_task|list_tasks|complete_task",
    "success": true,
    "message": "Human-readable result message",
    "data": { /* API response from executed skill */ }
  },
  "timestamp": "2026-01-09T16:00:00Z"
}
```

**Response Format** (Error):
```json
{
  "status": "error",
  "code": "SKILL_EXECUTION_ERROR",
  "message": "Human-readable error message",
  "details": { /* optional error details */ },
  "timestamp": "2026-01-09T16:00:00Z"
}
```

### 1.3 Skills Architecture

**Component Hierarchy**:
```
AI Endpoint Handler
├── Intent Detection (pattern matching)
├── Skill Router (intent → function mapping)
├── Skill Executors
│   ├── create_task (calls POST /users/{id}/tasks)
│   ├── list_tasks (calls GET /users/{id}/tasks)
│   └── complete_task (calls PATCH /users/{id}/tasks/{task_id}/complete)
└── Response Formatter
```

**State Management**:
- No persistent state (stateless processing)
- JWT token passed through to existing APIs
- User context maintained through existing authentication

### 1.4 Backend Integration Architecture

**Directory Structure**:
- `skills/todo_skills.py` - Core skill implementations and intent detection
- `skills/api.py` - FastAPI routes for AI endpoints
- `main.py` - Integration with existing application (new route inclusion)

**Integration Flow**:
1. User sends natural language request to `/api/ai/process`
2. Intent detection identifies skill (create_task, list_tasks, complete_task)
3. Skill executor calls existing Phase-2 API with JWT token
4. Response from Phase-2 API is formatted and returned

---
## Phase 2: Task Breakdown

**Output**: `tasks.md` (generated by `/sp.tasks` command)

Tasks will be grouped by component:

**P1 - Core Infrastructure**:
- Skills module setup
- Intent detection implementation
- JWT token handling

**P1 - Skill Implementations**:
- create_task skill
- list_tasks skill
- complete_task skill

**P1 - API Integration**:
- AI endpoints
- Response formatting
- Error handling

**P2 - Testing & Documentation**:
- Unit tests
- Integration tests
- Documentation

---
## Design Decision Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Intent Detection | Pattern matching with regex | Simple, fast, no ML dependencies |
| API Integration | HTTP calls to existing endpoints | Leverages existing functionality, maintains consistency |
| Authentication | Forward JWT tokens unchanged | Maintains security model, ensures user isolation |
| Architecture | Stateless service layer | Scalable, follows existing patterns |
| Skills Scope | Limited to create/list/complete | Focused, manageable implementation |

---
## Architectural Decision Records (ADRs)

The following decisions meet significance criteria and will require ADRs:

1. **ADR-001**: Pattern matching for intent detection vs. ML models (impact: complexity, maintenance)
2. **ADR-002**: Stateless AI layer vs. persistent context (impact: capabilities, scalability)

ADRs will be created during implementation when decisions are finalized.

---
## Implementation Phases Summary

| Phase | Deliverables | Duration |
|-------|--------------|----------|
| **Phase 0** | research.md with all decisions | Complete |
| **Phase 1** | data-model.md, API contracts, quickstart.md | Design complete |
| **Phase 2** | tasks.md with task breakdown | Approx 10-15 tasks |
| **Phase 3+** | Implementation per tasks.md | Iterative development |

---
## Next Steps

1. ✅ Specification complete (feature spec)
2. ✅ Implementation plan complete (`plan.md` - this file)
3. ⏭️ Run `/sp.tasks` to generate task breakdown
4. ⏭️ Begin implementation following task list
5. ⏭️ Each completed task updates corresponding tests

---
## Document Versioning

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-09 | Initial implementation plan for AI Skills Layer |