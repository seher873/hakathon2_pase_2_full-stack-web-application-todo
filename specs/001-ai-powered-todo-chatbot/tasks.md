---
description: "Task list for AI-Powered Todo Chatbot implementation"
---

# Tasks: AI-Powered Todo Chatbot

**Input**: Design documents from `/specs/001-ai-powered-todo-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Set up MCP SDK configuration in backend/mcp/
- [x] T002 Install OpenAI Agent SDK dependencies in backend requirements.txt
- [x] T003 [P] Configure OpenAI API environment variables in backend/.env

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create MCP tool interface layer in backend/mcp/task_tools.py
- [x] T005 [P] Create MCP authentication wrapper in backend/mcp/auth_wrapper.py
- [x] T006 [P] Create MCP tool registration in backend/mcp/tool_registry.py
- [x] T007 Create MCP tool models in backend/mcp/tool_models.py
- [x] T008 [P] Set up agent configuration in backend/agents/agent_config.py
- [x] T009 Configure agent API routes in backend/api/chat_routes.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Natural Language Task Creation (Priority: P1) 🎯 MVP

**Goal**: Users can create new tasks by typing natural language commands like "Add a task to submit report tomorrow" or "Create a task to buy groceries".

**Independent Test**: Can be fully tested by entering various natural language commands and verifying that appropriate tasks are created with correct details, delivering immediate value for task creation.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Contract test for chat creation endpoint in backend/tests/contract/test_chat_creation.py
- [ ] T011 [P] [US1] Integration test for task creation via chat in backend/tests/integration/test_task_creation_via_chat.py

### Implementation for User Story 1

- [x] T012 [P] [US1] Create create_task MCP tool in backend/mcp/task_tools.py
- [x] T013 [US1] Implement chatbot_agent for task creation in backend/agents/chatbot_agent.py
- [x] T014 [US1] Add chat panel component structure in frontend/src/components/chat/ChatPanel.jsx
- [x] T015 [US1] Add message input component in frontend/src/components/chat/MessageInput.jsx
- [x] T016 [US1] Add message display component in frontend/src/components/chat/ChatMessage.jsx
- [x] T017 [US1] Implement chat service for API communication in frontend/src/utils/chatService.js

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Management via Natural Language (Priority: P1)

**Goal**: Users can manage their existing tasks through natural language commands like "Mark my grocery task complete", "Show only pending tasks", or "Reschedule meeting to 2 PM".

**Independent Test**: Can be fully tested by issuing various task management commands and verifying they correctly update, filter, or modify tasks in the system.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T018 [P] [US2] Contract test for task management via chat in backend/tests/contract/test_task_management.py
- [ ] T019 [P] [US2] Integration test for updating tasks via chat in backend/tests/integration/test_task_update_via_chat.py

### Implementation for User Story 2

- [x] T020 [P] [US2] Create update_task MCP tool in backend/mcp/task_tools.py
- [x] T021 [P] [US2] Create list_tasks MCP tool in backend/mcp/task_tools.py
- [x] T022 [P] [US2] Create delete_task MCP tool in backend/mcp/task_tools.py
- [x] T023 [P] [US2] Create toggle_complete MCP tool in backend/mcp/task_tools.py
- [x] T024 [US2] Update chatbot_agent to handle multiple task operations in backend/agents/chatbot_agent.py
- [x] T025 [US2] Update message display to handle different operation results in frontend/src/components/chat/ChatMessage.jsx
- [x] T026 [US2] Add message formatting utilities in frontend/src/utils/messageFormatter.js

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Conversational Interface Integration (Priority: P2)

**Goal**: The chat interface is seamlessly integrated into the existing authenticated dashboard, providing real-time responses and maintaining conversation context.

**Independent Test**: Can be fully tested by accessing the chat interface from the dashboard and verifying that responses appear correctly and the UI matches the existing dashboard design.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T027 [P] [US3] Contract test for dashboard integration in frontend/tests/contract/test_chat_dashboard_integration.py
- [ ] T028 [P] [US3] Integration test for real-time responses in frontend/tests/integration/test_realtime_responses.py

### Implementation for User Story 3

- [x] T029 [US3] Integrate chat panel into authenticated dashboard layout in frontend/src/app/dashboard/page.tsx
- [x] T030 [US3] Add message list component in frontend/src/components/chat/MessageList.jsx
- [x] T031 [US3] Add typing indicator component in frontend/src/components/chat/TypingIndicator.jsx
- [x] T032 [US3] Implement response streaming in frontend/src/utils/chatService.js
- [x] T033 [US3] Add conversation context management in backend/agents/chatbot_agent.py
- [x] T034 [US3] Style chat components to match existing dashboard in frontend/src/styles/ChatPanel.css

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Secure Multi-User Isolation (Priority: P1)

**Goal**: The system maintains strict user isolation using JWT tokens from Better Auth, ensuring that users can only access and modify their own tasks through the chat interface.

**Independent Test**: Can be fully tested by verifying that JWT tokens are properly forwarded through the system and that users cannot access other users' tasks.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T035 [P] [US4] Contract test for JWT authentication in chat endpoints in backend/tests/contract/test_jwt_auth.py
- [ ] T036 [P] [US4] Integration test for user isolation in backend/tests/integration/test_user_isolation.py

### Implementation for User Story 4

- [x] T037 [US4] Implement JWT token forwarding from frontend to agent in frontend/src/utils/chatService.js
- [x] T038 [US4] Add authentication validation to chat routes in backend/api/chat_routes.py
- [x] T039 [US4] Validate JWT in MCP tools to ensure user isolation in backend/mcp/task_tools.py
- [x] T040 [US4] Update agent to operate within user's permission context in backend/agents/chatbot_agent.py
- [x] T041 [US4] Add error responses for access violations in backend/api/chat_routes.py
- [x] T042 [US4] Update frontend to handle authentication errors appropriately in frontend/src/components/chat/ChatPanel.jsx

**Checkpoint**: All user stories should now be independently functional with proper security

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T043 [P] Add documentation for chatbot API endpoints in docs/api/chatbot.md
- [x] T044 [P] Add documentation for MCP tool usage in docs/mcp-tools.md
- [x] T045 Add error handling and retry mechanisms in backend/agents/chatbot_agent.py
- [x] T046 Add logging for chat operations in backend/agents/chatbot_agent.py and backend/api/chat_routes.py
- [x] T047 [P] Add unit tests for agent and MCP tools in backend/tests/unit/
- [x] T048 Add comprehensive integration tests in backend/tests/integration/
- [x] T049 Update frontend to handle error states gracefully in frontend/src/components/chat/
- [x] T050 Run validation tests to ensure all user stories work together

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Builds on US1 agent functionality but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Builds on US1/US2 components but should be independently testable
- **User Story 4 (P1)**: Can start after Foundational (Phase 2) - Affects all previous stories but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for chat creation endpoint in backend/tests/contract/test_chat_creation.py"
Task: "Integration test for task creation via chat in backend/tests/integration/test_task_creation_via_chat.py"

# Launch all models for User Story 1 together:
Task: "Create create_task MCP tool in backend/mcp/task_tools.py"
Task: "Add message input component in frontend/src/components/chat/MessageInput.jsx"
Task: "Add message display component in frontend/src/components/chat/ChatMessage.jsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence