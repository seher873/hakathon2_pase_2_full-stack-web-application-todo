# AI Chatbot API Documentation

This document describes the API endpoints for the AI-powered todo chatbot.

## Base URL
All endpoints are prefixed with `/api/chat`

## Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## Endpoints

### POST /api/chat/message
Process a single chat message from the user.

#### Request Body
```json
{
  "message": "Add a task to submit report tomorrow",
  "user_id": "user123"
}
```

#### Response
```json
{
  "response": "Task 'Submit report' created successfully",
  "success": true,
  "data": {
    "task_id": 1,
    "title": "Submit report",
    "status": "pending"
  }
}
```

#### Example Request
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-jwt-token" \
  -d '{
    "message": "Add a task to buy groceries",
    "user_id": "user123"
  }'
```

### POST /api/chat/stream
Stream chat responses back to the client for real-time experience.

#### Request Body
```json
{
  "message": "Add a task to submit report tomorrow",
  "user_id": "user123"
}
```

#### Response
Server-Sent Events (SSE) stream with JSON data chunks.

#### Example Request
```bash
curl -X POST http://localhost:8000/api/chat/stream \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-jwt-token" \
  -d '{
    "message": "Show my pending tasks",
    "user_id": "user123"
  }'
```

### GET /api/chat/health
Health check endpoint for the chat API.

#### Response
```json
{
  "status": "healthy",
  "service": "chatbot-agent-api",
  "version": "1.0.0"
}
```

## Supported Natural Language Commands

The AI chatbot understands various natural language commands:

### Task Creation
- "Add a task to submit report tomorrow"
- "Create a task to buy groceries"
- "I need to schedule a meeting with John next week"

### Task Listing
- "Show my tasks"
- "What do I have left to do today?"
- "Show only pending tasks"
- "List completed tasks"

### Task Updates
- "Mark my grocery task complete"
- "Update the meeting time to 3 PM"
- "Change the due date of the report to Friday"

### Task Deletion
- "Delete the old task"
- "Remove the meeting from my list"

### Task Completion Toggle
- "Complete the shopping task"
- "Mark the assignment as done"
- "Toggle the status of the project task"

## Error Handling

Common error responses:

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "message"],
      "msg": "Field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Error processing chat message: description of the error"
}
```

## Examples

### Creating a Task
User: "Add a task to submit quarterly report by Friday"
- The system will extract the title ("submit quarterly report") and due date (this Friday)
- Creates a new task with these details

### Updating Task Status
User: "Mark the shopping task as complete"
- The system identifies the task containing "shopping"
- Updates the task status to "completed"

### Listing Tasks
User: "What do I have to do today?"
- The system lists all pending tasks due today

## Security Considerations

1. All requests must include a valid JWT token
2. Users can only access their own tasks
3. All inputs are validated through the MCP tool layer
4. The AI agent operates within the user's permission context
5. Authentication tokens are validated before any operations