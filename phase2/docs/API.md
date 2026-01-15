# API Documentation

## Base URL
`https://your-api-domain.com/api` (for production)
`http://localhost:8000/api` (for development)

## Authentication
All endpoints (except signup and login) require a valid JWT token in the Authorization header:
```
Authorization: Bearer {jwt_token}
```

## Common Response Format

### Success Response
```json
{
  "status": "success",
  "data": { /* response data */ },
  "timestamp": "2026-01-03T12:00:00Z"
}
```

### Error Response
```json
{
  "status": "error",
  "code": "ERROR_CODE",
  "message": "Human-readable error message",
  "details": { /* optional validation details */ },
  "timestamp": "2026-01-03T12:00:00Z"
}
```

## Endpoints

### Authentication

#### POST /auth/signup
Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "password_confirm": "SecurePassword123!"
}
```

**Responses:**
- `201 Created`: User created successfully
- `400 Bad Request`: Validation error (invalid email, weak password)
- `409 Conflict`: Email already registered
- `500 Internal Server Error`: Server error

#### POST /auth/login
Authenticate user and return JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Responses:**
- `200 OK`: User authenticated successfully
- `400 Bad Request`: Invalid credentials
- `401 Unauthorized`: Authentication failed
- `500 Internal Server Error`: Server error

### Tasks

#### GET /users/{user_id}/tasks
Get all tasks for a user.

**Query Parameters:**
- `completed` (boolean, optional): Filter by completion status
- `search` (string, optional): Search term for title or description
- `limit` (integer, optional): Max number of tasks to return (1-1000, default: 100)
- `offset` (integer, optional): Number of tasks to skip (default: 0)

**Responses:**
- `200 OK`: Tasks retrieved successfully
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: User cannot access this resource
- `500 Internal Server Error`: Server error

#### POST /users/{user_id}/tasks
Create a new task for a user.

**Request Body:**
```json
{
  "title": "Task title",
  "description": "Task description (optional)"
}
```

**Responses:**
- `201 Created`: Task created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: User cannot access this resource
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

#### GET /users/{user_id}/tasks/{task_id}
Get a specific task.

**Responses:**
- `200 OK`: Task retrieved successfully
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: User cannot access this resource
- `404 Not Found`: Task not found
- `500 Internal Server Error`: Server error

#### PUT /users/{user_id}/tasks/{task_id}
Update an existing task.

**Request Body:**
```json
{
  "title": "Updated title (optional)",
  "description": "Updated description (optional)"
}
```

**Responses:**
- `200 OK`: Task updated successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: User cannot access this resource
- `404 Not Found`: Task not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

#### PATCH /users/{user_id}/tasks/{task_id}/complete
Update task completion status.

**Request Body:**
```json
{
  "completed": true
}
```

**Responses:**
- `200 OK`: Task completion status updated successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: User cannot access this resource
- `404 Not Found`: Task not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

#### DELETE /users/{user_id}/tasks/{task_id}
Delete a task.

**Responses:**
- `204 No Content`: Task deleted successfully
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: User cannot access this resource
- `404 Not Found`: Task not found
- `500 Internal Server Error`: Server error

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| INVALID_EMAIL | 400 | Email format is invalid |
| WEAK_PASSWORD | 400 | Password doesn't meet requirements |
| PASSWORD_MISMATCH | 400 | Passwords don't match |
| DUPLICATE_EMAIL | 409 | Email already registered |
| UNAUTHORIZED_ACCESS | 401 | Invalid or missing token |
| FORBIDDEN_ACCESS | 403 | User cannot access this resource |
| TASK_NOT_FOUND | 404 | Task doesn't exist |
| VALIDATION_ERROR | 422 | Request validation failed |
| SERVER_ERROR | 500 | Internal server error |