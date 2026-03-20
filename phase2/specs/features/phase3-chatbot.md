# Phase 3: AI-Powered Todo Chatbot Specification

**Feature Branch**: `phase3-chatbot`
**Created**: 2026-03-20
**Status**: In Progress
**Phase**: III - AI Chatbot with MCP & OpenAI Agents

---

## Overview

Build an AI-powered chatbot interface for managing todos through natural language using:
- **OpenAI Agents SDK** for AI logic
- **MCP (Model Context Protocol) Server** for task operations as tools
- **OpenAI ChatKit** for frontend UI
- **Stateless architecture** with database persistence

---

## Requirements

### Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-301 | System MUST provide conversational interface for all Basic Level features | P1 |
| FR-302 | System MUST use OpenAI Agents SDK for AI logic | P1 |
| FR-303 | System MUST build MCP server with Official MCP SDK | P1 |
| FR-304 | System MUST expose task operations as MCP tools | P1 |
| FR-305 | System MUST persist conversation state to database | P1 |
| FR-306 | System MUST be stateless (no in-memory state) | P1 |
| FR-307 | AI agents MUST use MCP tools to manage tasks | P1 |

### MCP Tools Specification

| Tool | Purpose | Parameters | Returns |
|------|---------|------------|---------|
| `add_task` | Create new task | user_id, title, description | task_id, status, title |
| `list_tasks` | Retrieve tasks | user_id, status (optional) | Array of task objects |
| `complete_task` | Mark task complete | user_id, task_id | task_id, status, title |
| `delete_task` | Remove task | user_id, task_id | task_id, status, title |
| `update_task` | Modify task | user_id, task_id, title, description | task_id, status, title |

### Natural Language Commands

| User Says | Agent Should |
|-----------|--------------|
| "Add a task to buy groceries" | Call add_task with title "Buy groceries" |
| "Show me all my tasks" | Call list_tasks with status "all" |
| "What's pending?" | Call list_tasks with status "pending" |
| "Mark task 3 as complete" | Call complete_task with task_id 3 |
| "Delete the meeting task" | Call list_tasks first, then delete_task |
| "Change task 1 to 'Call mom tonight'" | Call update_task with new title |
| "I need to remember to pay bills" | Call add_task with title "Pay bills" |
| "What have I completed?" | Call list_tasks with status "completed" |

---

## Database Models

### Conversation Model
| Field | Type | Description |
|-------|------|-------------|
| id | str (UUID) | Primary key |
| user_id | str | Owner of conversation |
| created_at | datetime | Creation timestamp |
| updated_at | datetime | Last update timestamp |

### Message Model
| Field | Type | Description |
|-------|------|-------------|
| id | str (UUID) | Primary key |
| user_id | str | Message author |
| conversation_id | str (UUID) | Parent conversation |
| role | str | "user" or "assistant" |
| content | str | Message content |
| created_at | datetime | Message timestamp |

---

## API Endpoints

### POST /api/chat
Send message and get AI response.

**Request:**
```json
{
  "conversation_id": "optional-uuid",
  "message": "Add a task to buy milk"
}
```

**Response:**
```json
{
  "conversation_id": "uuid",
  "response": "I've added 'Buy milk' to your tasks!",
  "tool_calls": [
    {"tool": "add_task", "result": {"task_id": "123", "status": "created"}}
  ]
}
```

### GET /api/conversations
List user's conversations.

### GET /api/conversations/{id}/messages
Get conversation history.

### DELETE /api/conversations/{id}
Delete a conversation.

---

## Agent Behavior Specification

| Behavior | Description |
|----------|-------------|
| Task Creation | When user mentions adding/creating/remembering, use add_task |
| Task Listing | When user asks to see/show/list, use list_tasks |
| Task Completion | When user says done/complete/finished, use complete_task |
| Task Deletion | When user says delete/remove/cancel, use delete_task |
| Task Update | When user says change/update/rename, use update_task |
| Confirmation | Always confirm actions with friendly response |
| Error Handling | Gracefully handle task not found and other errors |

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Frontend | OpenAI ChatKit |
| Backend | Python FastAPI |
| AI Framework | OpenAI Agents SDK |
| MCP Server | Official MCP SDK |
| ORM | SQLModel |
| Database | SQLite (dev) / Neon PostgreSQL (prod) |

---

## Success Criteria

| ID | Criteria | Measurement |
|----|----------|-------------|
| SC-301 | Chatbot responds to natural language commands | 90%+ intent recognition accuracy |
| SC-302 | MCP tools execute correctly | 100% tool execution success |
| SC-303 | Conversations persist in database | Verified via DB query |
| SC-304 | Server is stateless | Restart doesn't lose data |
| SC-305 | Chat UI is responsive | Works on mobile and desktop |

---

## Assumptions

- OpenAI API key is available via environment variable
- Users are authenticated before accessing chat
- Database is properly initialized with tables

---

## Dependencies

- `openai-agents` - OpenAI Agents SDK
- `mcp` - Official MCP SDK
- `fastapi` - Web framework
- `sqlmodel` - Database ORM
- `sqlalchemy` - Database toolkit

---

## Out of Scope (Phase 3)

- Voice commands (Phase 5 bonus)
- Multi-language support (Phase 5 bonus)
- Advanced NLP features (recurring tasks, due dates)
- Real-time sync across clients

---

## Document Versioning

| Version | Date | Notes |
|---------|------|-------|
| 1.0 | 2026-03-20 | Initial specification |
