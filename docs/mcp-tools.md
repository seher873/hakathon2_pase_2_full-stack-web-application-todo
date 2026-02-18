# MCP Tools Documentation

This document describes the Model Context Protocol (MCP) tools used in the AI-powered todo chatbot.

## Overview

MCP tools are functions that the AI agent can call to perform specific actions. In our system, these tools wrap the existing FastAPI endpoints to provide a secure and authenticated interface between the AI agent and the backend services.

## Tool Registration

All tools are registered in the `ToolRegistry` class in `backend/mcp/tool_registry.py`. The registry maintains:
- Tool functions
- Tool signatures in JSON Schema format
- Access validation mechanisms

## Available Tools

### create_task
Creates a new task.

#### Signature
```json
{
  "type": "function",
  "function": {
    "name": "create_task",
    "description": "Create a new task with title, description, and optional due date",
    "parameters": {
      "type": "object",
      "properties": {
        "title": {
          "type": "string",
          "description": "The title of the task"
        },
        "description": {
          "type": "string",
          "description": "Optional description of the task"
        },
        "due_date": {
          "type": "string",
          "description": "Optional due date in YYYY-MM-DD format"
        }
      },
      "required": ["title"]
    }
  }
}
```

#### Usage
Called when the user requests to create a new task. The AI agent extracts the title, description, and due date from the natural language request.

### list_tasks
Lists tasks with optional filtering.

#### Signature
```json
{
  "type": "function",
  "function": {
    "name": "list_tasks",
    "description": "List tasks with optional filtering by status",
    "parameters": {
      "type": "object",
      "properties": {
        "filter_by": {
          "type": "string",
          "description": "Optional filter criteria"
        },
        "status": {
          "type": "string",
          "enum": ["pending", "completed", "all"],
          "description": "Filter tasks by status"
        }
      }
    }
  }
}
```

#### Usage
Called when the user requests to view their tasks. Can filter by status (pending, completed, all) or other criteria.

### update_task
Updates an existing task.

#### Signature
```json
{
  "type": "function",
  "function": {
    "name": "update_task",
    "description": "Update an existing task",
    "parameters": {
      "type": "object",
      "properties": {
        "task_id": {
          "type": "integer",
          "description": "ID of the task to update"
        },
        "title": {
          "type": "string",
          "description": "New title for the task"
        },
        "description": {
          "type": "string",
          "description": "New description for the task"
        },
        "due_date": {
          "type": "string",
          "description": "New due date in YYYY-MM-DD format"
        },
        "status": {
          "type": "string",
          "enum": ["pending", "completed"],
          "description": "New status for the task"
        }
      },
      "required": ["task_id"]
    }
  }
}
```

#### Usage
Called when the user requests to update a task. Requires the task ID and can update any of the other fields.

### delete_task
Deletes a task.

#### Signature
```json
{
  "type": "function",
  "function": {
    "name": "delete_task",
    "description": "Delete a task by ID",
    "parameters": {
      "type": "object",
      "properties": {
        "task_id": {
          "type": "integer",
          "description": "ID of the task to delete"
        }
      },
      "required": ["task_id"]
    }
  }
}
```

#### Usage
Called when the user requests to delete a task. Requires the task ID.

### toggle_complete
Toggles the completion status of a task.

#### Signature
```json
{
  "type": "function",
  "function": {
    "name": "toggle_complete",
    "description": "Toggle the completion status of a task",
    "parameters": {
      "type": "object",
      "properties": {
        "task_id": {
          "type": "integer",
          "description": "ID of the task to toggle"
        }
      },
      "required": ["task_id"]
    }
  }
}
```

#### Usage
Called when the user requests to toggle a task's completion status. Requires the task ID.

## Security and Authentication

Each MCP tool call includes the user's JWT token to ensure:
1. The user is authenticated
2. The user can only perform operations on their own tasks
3. All existing authorization checks are maintained

The token is passed through the following flow:
1. Frontend includes token in chat request
2. Backend validates token via `auth_wrapper.verify_token`
3. Token is forwarded to MCP tools via `forward_token_to_mcp_tools`
4. Each tool uses the token to make authenticated requests to the existing FastAPI endpoints

## Implementation Details

### Tool Execution Flow
1. AI agent determines which tool to call based on user request
2. Tool parameters are extracted from the natural language
3. Token is validated and forwarded to the tool
4. Tool executes the action on the existing backend
5. Result is returned to the AI agent
6. AI agent formulates a natural language response

### Error Handling
If a tool execution fails, the error is:
1. Caught and logged
2. Formatted into a user-friendly message
3. Returned to the AI agent
4. Communicated to the user in a natural way

## Adding New Tools

To add a new MCP tool:

1. Implement the tool function in `backend/mcp/task_tools.py`
2. Add the tool signature to `backend/mcp/tool_registry.py`
3. Ensure proper authentication and authorization checks
4. Test the tool with various inputs
5. Update this documentation

## Best Practices

1. Keep tool functions focused and single-purpose
2. Validate all inputs before making backend calls
3. Handle errors gracefully and provide meaningful messages
4. Preserve user authentication context throughout the operation
5. Maintain consistency with existing API patterns