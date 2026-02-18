# Implementation Plan: AI-Powered Todo Chatbot

**Feature**: 001-ai-powered-todo-chatbot
**Created**: 2026-02-17
**Status**: Draft
**Spec Reference**: specs/001-ai-powered-todo-chatbot/spec.md

## 1. IMPLEMENTATION OVERVIEW

The AI-Powered Todo Chatbot will be implemented as an additional layer that sits between the frontend chat interface and the existing Phase II backend. The system will maintain all existing CRUD functionality while adding conversational capabilities through natural language processing.

**Integration Strategy**: The AI layer will reuse existing FastAPI endpoints and business logic, acting as an orchestration layer that translates natural language commands into standard API calls. This ensures no duplication of business logic while providing a conversational interface.

**Architecture**: The implementation will follow the pattern: User Message → Chat Interface → AI Agent → MCP Tools → Existing FastAPI Endpoints → Database.

## 2. ARCHITECTURE IMPACT ANALYSIS

### What Remains Unchanged:
- FastAPI backend with existing task CRUD endpoints
- Neon PostgreSQL database schema and structure
- Better Auth authentication system and JWT handling
- Frontend dashboard and existing UI components
- Database connection logic and models

### What New Layers Are Introduced:
- MCP tool interface layer that wraps existing FastAPI endpoints
- OpenAI Agent orchestration layer that processes natural language
- Chat interface components that integrate into existing dashboard
- Authentication propagation mechanism from frontend to agent to backend

### Clear Boundary Definition:
**Agent Layer**: Handles natural language processing, intent recognition, and tool selection
**Backend Logic**: Remains in FastAPI with existing business rules and validation
**Communication**: MCP tools serve as the interface layer between agent and backend

## 3. MCP TOOL MAPPING PLAN

Each MCP tool will wrap an existing FastAPI endpoint while preserving authentication and validation:

- **create_task(title, description, due_date)** → POST /api/tasks (existing endpoint)
  - Maps natural language inputs to task creation parameters
  - Preserves JWT-based user association
  - Maintains existing validation rules

- **list_tasks(filter, status)** → GET /api/tasks (existing endpoint)
  - Maps natural language filters to query parameters
  - Maintains user isolation through JWT
  - Preserves pagination and response format

- **update_task(id, fields)** → PUT /api/tasks/{id} (existing endpoint)
  - Maps natural language updates to specific fields
  - Validates user ownership of task
  - Preserves existing update validation

- **delete_task(id)** → DELETE /api/tasks/{id} (existing endpoint)
  - Maps natural language to task identification
  - Validates user ownership before deletion
  - Maintains existing authorization checks

- **toggle_complete(id)** → PATCH /api/tasks/{id} (existing endpoint)
  - Maps "complete/incomplete" language to boolean updates
  - Maintains user isolation and validation
  - Preserves existing status update logic

## 4. AGENT EXECUTION FLOW

### Lifecycle Definition:
```
User Message (natural language)
→ ChatKit UI (Next.js component)
→ OpenAI Agent (intent parsing and tool selection)
→ MCP Tools (authentication-aware API calls)
→ FastAPI Backend (existing business logic)
→ Database (existing persistence layer)
→ Response Streamed Back to Chat Interface
```

### Authentication Flow:
- JWT token is passed from Next.js frontend to agent
- Agent includes token when calling MCP tools
- MCP tools forward token to FastAPI endpoints
- All user isolation is maintained through existing authentication system

### Error Handling:
- Natural language processing errors return to user as helpful messages
- API errors are propagated through the chain to the UI
- Network failures have retry mechanisms at the tool interface layer

## 5. FRONTEND INTEGRATION PLAN

### Components to Create:
- **ChatPanel Component**: Integrated into existing dashboard layout
- **MessageList Component**: Displays conversation history
- **MessageInput Component**: Handles user input and response streaming
- **MessageDisplay Component**: Renders both user and system messages

### Integration Points:
- Add chat interface to authenticated user dashboard
- Maintain existing UI alongside chat functionality
- Ensure responsive design matches existing application
- Preserve navigation and user session management

### Streaming Responses:
- Implement real-time message streaming using ChatKit
- Display typing indicators during processing
- Handle partial responses appropriately
- Manage connection states and potential timeouts

### No Direct API Replacement:
- Chat interface calls agent layer exclusively
- Existing task UI remains functional
- Both interfaces can be used simultaneously
- All data operations flow through existing backend

## 6. AUTHENTICATION PROPAGATION PLAN

### JWT Flow:
```
Next.js Authenticated Session
→ Chat Interface Component
→ Agent API Call (with JWT token)
→ MCP Tool Layer (token forwarding)
→ FastAPI Auth Middleware
→ User-specific Data Access
```

### Token Management:
- JWT token is securely stored in frontend
- Token is passed with each agent request
- MCP layer forwards token to backend services
- All existing authentication checks remain in place

### Security Measures:
- No anonymous agent execution
- All operations validated against user identity
- Task access limited to owner via existing middleware
- API rate limiting preserved at existing layer

### User Isolation:
- Agent operates within user's permission context
- MCP tools enforce user-task association
- No cross-user data access possible
- All existing security models remain unchanged

## 7. FILE-LEVEL CHANGE PLAN

### New Backend Directories:
```
/backend/agents/
  - chatbot_agent.py (OpenAI Agent definition)
  - agent_config.py (Configuration and settings)
  - intent_classifier.py (Optional: custom intent processing)

/backend/mcp/
  - task_tools.py (MCP tool definitions for task operations)
  - auth_wrapper.py (Authentication forwarding utilities)
  - tool_registry.py (Tool registration and management)
  - tool_models.py (Pydantic models for tool parameters)

/backend/api/
  - chat_routes.py (New chat API endpoints to serve agent)
```

### New Frontend Components:
```
/frontend/src/components/chat/
  - ChatPanel.jsx (Main chat interface container)
  - MessageList.jsx (Conversation history display)
  - MessageInput.jsx (User input field with streaming)
  - ChatMessage.jsx (Individual message display)
  - TypingIndicator.jsx (Loading state visualization)

/frontend/src/utils/
  - chatService.js (Chat API communication)
  - messageFormatter.js (Response formatting utilities)
```

### Integration with Existing Architecture:
- No changes to existing database models
- No modifications to existing task CRUD endpoints
- New endpoints will follow existing patterns and conventions
- All new components will use existing styling system (Tailwind)

## 8. IMPLEMENTATION ORDER (CRITICAL)

### Step 1 — Add MCP Wrapper Layer
- Create MCP tool definitions that wrap existing API endpoints
- Implement authentication forwarding in tool layer
- Set up error handling and validation for tool calls
- Ensure all existing authentication checks remain functional

### Step 2 — Register Tools with Agent SDK
- Define OpenAI Agent with appropriate tools
- Configure agent for our specific task management domain
- Set up agent configuration and system instructions
- Implement basic natural language understanding

### Step 3 — Connect Agent to FastAPI
- Create new chat API endpoints to interface with agent
- Implement JWT token forwarding from frontend
- Add authentication middleware for agent endpoints
- Ensure proper error propagation from agent to UI

### Step 4 — Build Chat UI Shell
- Create basic chat interface components
- Integrate chat panel into existing dashboard layout
- Implement basic message display functionality
- Add input field with submission handling

### Step 5 — Enable Streaming Responses
- Implement real-time response streaming
- Add typing indicators and loading states
- Handle partial message updates
- Manage connection and error states

### Step 6 — Wire Authentication Context
- Implement JWT token passing from UI to agent
- Ensure user isolation in all operations
- Test authentication flow end-to-end
- Verify user-specific data access

### Step 7 — Validate Conversational CRUD
- Test all task operations via natural language
- Verify user isolation in chat operations
- Confirm all existing functionality remains intact
- Conduct end-to-end testing of chat interface

## 9. VALIDATION STRATEGY

### Functional Validation:
- **Natural Language Task Creation**: Verify commands like "Add a task to submit report tomorrow" create appropriate tasks
- **Task Updates via Chat**: Test commands like "Mark my grocery task complete" correctly update task status
- **Task Filtering**: Validate "Show only pending tasks" returns correct results
- **Deadline Recognition**: Confirm "Reschedule meeting to 2 PM" updates due dates properly

### Security Validation:
- **User Isolation**: Ensure users can only access their own tasks via chat
- **Authentication Flow**: Verify JWT tokens are properly forwarded through all layers
- **API Security**: Confirm existing security measures remain effective
- **Data Integrity**: Test that chat operations don't corrupt existing data

### Performance Validation:
- **Response Time**: Verify acceptable response times for natural language processing
- **Concurrent Users**: Test multiple users using chat simultaneously
- **Connection Management**: Validate streaming connections function properly
- **Error Recovery**: Ensure system gracefully handles various failure modes

### Integration Validation:
- **Coexistence**: Verify chat interface works alongside existing UI
- **Data Consistency**: Confirm same data appears in both UI and chat
- **Synchronization**: Test that changes via chat update other UI elements
- **Backwards Compatibility**: Ensure existing functionality remains intact

## 10. NON-GOALS (TO PREVENT SCOPE CREEP)

### What This Plan Will NOT Include:
- **Replace Backend**: Do not rebuild or replace existing FastAPI backend
- **Add Alternative Frameworks**: Do not introduce LangChain, LlamaIndex, or other AI frameworks
- **Modify Database Schema**: Do not alter existing PostgreSQL schema unnecessarily
- **Rebuild Authentication**: Do not replace Better Auth system with alternatives
- **Change Database Technology**: Do not switch from Neon PostgreSQL to other databases
- **Add New Frontend Technologies**: Do not introduce new UI frameworks beyond Next.js/React
- **Modify Existing Endpoints**: Do not change existing task CRUD API behavior
- **Add External Services**: Do not require additional third-party services beyond OpenAI and MCP

### Scope Boundaries:
- Focus purely on adding conversational interface
- Maintain all existing business logic and validation
- Reuse all existing authentication and authorization
- Preserve all existing data models and schemas
- Integrate rather than replace existing components
- Keep changes to a minimum viable implementation
- Prioritize security and user isolation
- Maintain backward compatibility with existing UI