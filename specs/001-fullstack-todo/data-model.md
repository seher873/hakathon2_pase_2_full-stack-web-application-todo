# Data Model: AI Skills Layer for Todo Application

**Date**: 2026-01-09
**Feature**: AI Skills Preview
**Input**: Feature specification and implementation plan

## Overview

The AI Skills layer does not introduce new data models. It leverages existing Phase-2 data models through API calls. This document describes how the AI Skills layer interfaces with existing data structures.

## Existing Data Models (No New Models Required)

### User Model (via API)
- **Source**: Phase-2 backend `/src/models/user.py`
- **Fields used by AI Skills**:
  - `id`: UUID - User identifier for authentication
  - `email`: String - User email (for reference only)

### Task Model (via API)
- **Source**: Phase-2 backend `/src/models/task.py`
- **Fields used by AI Skills**:
  - `id`: UUID - Task identifier
  - `title`: String - Task title (required)
  - `description`: String (optional) - Task description
  - `completed`: Boolean - Completion status
  - `user_id`: UUID - Foreign key to user
  - `created_at`: DateTime - Creation timestamp
  - `updated_at`: DateTime - Update timestamp

## AI Skills Request/Response Models

### AI Request Model
```json
{
  "input": "Natural language request (e.g., 'Add buy milk')"
}
```

**Validation Rules**:
- `input` is required
- `input` must be non-empty string
- `input` max length: 1000 characters

### AI Response Model
```json
{
  "status": "success|error",
  "data": {
    "skill": "create_task|list_tasks|complete_task|unknown",
    "success": true|false,
    "message": "Human-readable result message",
    "data": { /* API response from executed skill */ }
  },
  "timestamp": "2026-01-09T16:00:00Z"
}
```

**Validation Rules**:
- `status` is required (success or error)
- `data` object is required
- `skill` is required when success=true
- `success` is required boolean
- `message` is required human-readable string
- `timestamp` is required ISO format

## API Request/Response Mapping

### create_task Skill
- **AI Input**: "Add buy milk" or "Create task finish report"
- **API Request**: `POST /users/{user_id}/tasks`
```json
{
  "title": "buy milk",
  "description": null
}
```
- **API Response**: TaskResponse object
- **AI Output**: Success with task details

### list_tasks Skill
- **AI Input**: "Show my tasks" or "List my tasks"
- **API Request**: `GET /users/{user_id}/tasks`
- **API Response**: TaskListResponse object
- **AI Output**: Success with list of tasks

### complete_task Skill
- **AI Input**: "Complete buy milk" or "Mark report done"
- **API Request**: `PATCH /users/{user_id}/tasks/{task_id}/complete`
```json
{
  "completed": true
}
```
- **API Response**: TaskResponse object
- **AI Output**: Success with updated task

## State Management

### No Persistent State
- The AI Skills layer is stateless
- All user data is stored in the existing backend
- JWT tokens are passed through without modification
- No caching implemented (for Phase 3 preview)

### Authentication Flow
1. JWT token extracted from request headers by existing middleware
2. Token forwarded unchanged to existing API calls
3. User isolation maintained by existing backend logic
4. No additional authentication state stored

## Validation Rules

### Input Validation
- Natural language input must be non-empty
- Input length limited to 1000 characters to prevent abuse
- Skill detection validates that detected skill is supported

### Output Validation
- All responses follow standard SuccessResponse/ErrorResponse format
- Error messages are user-friendly
- API responses are validated before forwarding

## Relationships

### Data Flow Relationships
```
User Input (natural language)
  ↓
Intent Detection (regex matching)
  ↓
Skill Selection (create_task|list_tasks|complete_task)
  ↓
API Call (to existing Phase-2 endpoints)
  ↓
Response Formatting (standard response format)
  ↓
User Output
```

### Security Relationships
- AI Skills → JWT Token: Forward unchanged
- AI Skills → User Data: Read/Write only through existing APIs
- AI Skills → Task Data: Manipulate only through existing APIs

## Schema Evolution

### Backward Compatibility
- AI Skills layer designed to work with existing API schemas
- No breaking changes to Phase-2 data models
- New skills can be added without changing existing schemas

### Future Extensions
- Additional skills can be added following the same pattern
- Natural language patterns can be extended without schema changes
- Response format can accommodate new skill types

## Constraints

### Data Integrity
- All data modifications go through existing API validation
- User isolation enforced by existing backend logic
- No direct database access from AI Skills layer

### Performance Constraints
- API calls must complete within existing timeout limits
- No additional database queries beyond existing APIs
- Response formatting should add minimal overhead (<50ms)

## Indexes and Performance Considerations

### Existing Indexes Used
- User ID indexes for authentication (from existing models)
- Task user_id indexes for data isolation (from existing models)

### No New Indexes Required
- AI Skills layer does not create new database tables
- Performance depends on existing API performance
- Caching may be added in future phases if needed

## Document Versioning

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-09 | Initial data model for AI Skills Layer |