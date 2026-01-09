# AI Skills for Todo Application - Phase 3 Preview

⚠️ **PREVIEW FEATURE** - This module is part of Phase 3 preview and does not impact Phase 2 grading requirements.

This module provides natural language processing capabilities to map user requests to backend API calls.

## Overview

The AI Skills layer allows users to interact with the Todo application using natural language. It maps user inputs to the appropriate backend API calls while respecting JWT-based authentication and user isolation.

## Supported Skills

### 1. create_task
- **Purpose**: Create a new task
- **Patterns**:
  - "Add buy milk"
  - "Create task finish report"
  - "New task call mom"
  - "Task buy groceries"
  - "Add task clean house - with supplies"

### 2. list_tasks
- **Purpose**: List all tasks for the user
- **Patterns**:
  - "Show my tasks"
  - "List my tasks"
  - "View my tasks"
  - "What tasks do I have?"
  - "All tasks"

### 3. complete_task
- **Purpose**: Mark a task as complete
- **Patterns**:
  - "Complete buy milk"
  - "Finish report task"
  - "Mark grocery shopping done"
  - "Check finish report"

## Architecture

- Skills are implemented in `todo_skills.py`
- API endpoints are exposed in `api.py`
- All skills respect JWT authentication and user isolation
- Skills call existing Phase-2 APIs, they don't access the database directly

## API Endpoints

The AI Skills are accessible via the following endpoints:

### Process Natural Language Request
`POST /api/ai/process`

Request:
```json
{
  "input": "Add buy milk"
}
```

Response:
```json
{
  "status": "success",
  "data": {
    "skill": "create_task",
    "success": true,
    "message": "Task 'buy milk' created successfully",
    "data": { ... }
  },
  "timestamp": "2026-01-09T16:00:00Z"
}
```

### List Available Skills
`GET /api/ai/skills`

Response:
```json
{
  "status": "success",
  "data": [
    {
      "name": "create_task",
      "description": "Create a new task",
      "examples": [
        "Add buy milk",
        "Create task finish report",
        "New task call mom"
      ]
    },
    {
      "name": "list_tasks",
      "description": "List all your tasks",
      "examples": [
        "Show my tasks",
        "List my tasks",
        "What tasks do I have?"
      ]
    },
    {
      "name": "complete_task",
      "description": "Mark a task as complete",
      "examples": [
        "Complete buy milk",
        "Finish report task",
        "Mark grocery shopping done"
      ]
    }
  ],
  "timestamp": "2026-01-09T16:00:00Z"
}
```

## Implementation Details

- Uses regex patterns to match user intent
- Integrates with existing backend services
- Maintains user isolation through JWT validation
- Follows the same error handling patterns as the rest of the API