# API Contract: Phase-2 Backend

## Version Information
- **API Version**: 1.0
- **Contract Date**: 2026-01-17
- **Base URL**: http://localhost:4000 (or configured server URL)

## Authentication
All protected endpoints require JWT Bearer token authentication:
```
Authorization: Bearer <jwt-token>
```

## Common Response Format
Successful responses follow this structure:
```json
{
  "message": "Descriptive message",
  "data": { /* response data */ },
  "timestamp": "ISO 8601 timestamp"
}
```

Error responses follow this structure:
```json
{
  "error": "Error message",
  "message": "Additional details",
  "timestamp": "ISO 8601 timestamp"
}
```

## Endpoints

### Authentication Service

#### POST /api/auth/register
**Description**: Register a new user account
**Authentication**: None required

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Request Validation**:
- email: Required, valid email format
- password: Required, minimum length enforced

**Successful Response (201)**:
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "createdAt": "2026-01-17T09:31:54.489Z"
  },
  "token": "jwt_token_string"
}
```

**Error Responses**:
- 400: Invalid input (missing fields, invalid email)
- 409: Email already exists
- 500: Server error

#### POST /api/auth/login
**Description**: Authenticate user and return token
**Authentication**: None required

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Request Validation**:
- email: Required, valid email format
- password: Required

**Successful Response (200)**:
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "email": "user@example.com"
  },
  "token": "jwt_token_string"
}
```

**Error Responses**:
- 400: Missing email or password
- 401: Invalid credentials
- 500: Server error

#### POST /api/auth/logout
**Description**: Logout user (client-side token invalidation)
**Authentication**: Bearer token required

**Successful Response (200)**:
```json
{
  "message": "Logged out successfully"
}
```

**Error Responses**:
- 401: Invalid or expired token
- 500: Server error

#### GET /api/auth/me
**Description**: Get authenticated user information
**Authentication**: Bearer token required

**Successful Response (200)**:
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": null,
    "createdAt": "2026-01-17T09:31:54.489Z",
    "updatedAt": "2026-01-17T09:31:54.489Z"
  }
}
```

**Error Responses**:
- 401: Unauthorized, no active session
- 500: Server error

### Tasks Service

#### GET /api/tasks
**Description**: Get all tasks for authenticated user
**Authentication**: Bearer token required

**Successful Response (200)**:
```json
{
  "data": [
    {
      "id": 1,
      "user_id": 1,
      "title": "Sample Task",
      "description": "This is a sample task",
      "status": "todo",
      "created_at": "2026-01-17T09:31:54.489Z",
      "updated_at": "2026-01-17T09:31:54.489Z"
    }
  ],
  "message": "Tasks retrieved successfully"
}
```

**Error Responses**:
- 401: Unauthorized, no active session
- 500: Server error

#### POST /api/tasks
**Description**: Create a new task for authenticated user
**Authentication**: Bearer token required

**Request Body**:
```json
{
  "title": "New Task",
  "description": "Detailed task description",
  "status": "todo"
}
```

**Request Validation**:
- title: Required
- description: Optional
- status: Optional, defaults to 'todo'

**Successful Response (201)**:
```json
{
  "data": {
    "id": 2,
    "user_id": 1,
    "title": "New Task",
    "description": "Detailed task description",
    "status": "todo",
    "created_at": "2026-01-17T09:32:15.234Z",
    "updated_at": "2026-01-17T09:32:15.234Z"
  },
  "message": "Task created successfully"
}
```

**Error Responses**:
- 400: Missing title
- 401: Unauthorized, no active session
- 500: Server error

#### GET /api/tasks/{id}
**Description**: Get a specific task for authenticated user
**Authentication**: Bearer token required

**Parameters**:
- id: Task ID (path parameter)

**Successful Response (200)**:
```json
{
  "data": {
    "id": 1,
    "user_id": 1,
    "title": "Sample Task",
    "description": "This is a sample task",
    "status": "todo",
    "created_at": "2026-01-17T09:31:54.489Z",
    "updated_at": "2026-01-17T09:31:54.489Z"
  },
  "message": "Task retrieved successfully"
}
```

**Error Responses**:
- 401: Unauthorized, no active session
- 404: Task not found or does not belong to user
- 500: Server error

#### PUT /api/tasks/{id}
**Description**: Update a specific task for authenticated user
**Authentication**: Bearer token required

**Parameters**:
- id: Task ID (path parameter)

**Request Body**:
```json
{
  "title": "Updated Task Title",
  "description": "Updated description",
  "status": "in-progress"
}
```

**Request Validation**:
- At least one field required
- status: If provided, must be valid value

**Successful Response (200)**:
```json
{
  "data": {
    "id": 1,
    "user_id": 1,
    "title": "Updated Task Title",
    "description": "Updated description",
    "status": "in-progress",
    "created_at": "2026-01-17T09:31:54.489Z",
    "updated_at": "2026-01-17T09:35:22.123Z"
  },
  "message": "Task updated successfully"
}
```

**Error Responses**:
- 400: Invalid input
- 401: Unauthorized, no active session
- 404: Task not found or does not belong to user
- 500: Server error

#### DELETE /api/tasks/{id}
**Description**: Delete a specific task for authenticated user
**Authentication**: Bearer token required

**Parameters**:
- id: Task ID (path parameter)

**Successful Response (200)**:
```json
{
  "message": "Task deleted successfully"
}
```

**Error Responses**:
- 401: Unauthorized, no active session
- 404: Task not found or does not belong to user
- 500: Server error

### Health Check Service

#### GET /api/health/ping
**Description**: Simple health check
**Authentication**: None required

**Successful Response (200)**:
```json
{
  "message": "Pong!",
  "timestamp": "2026-01-17T09:31:54.489Z"
}
```

#### GET /api/health/status
**Description**: Detailed health status
**Authentication**: None required

**Successful Response (200)**:
```json
{
  "status": "healthy",
  "service": "Hackathon Phase 2 Backend",
  "version": "1.0.0",
  "environment": "development",
  "timestamp": "2026-01-17T09:31:54.489Z"
}
```

#### GET /api/status
**Description**: Alternative status endpoint
**Authentication**: None required

**Successful Response (200)**:
```json
{
  "status": "healthy",
  "service": "Hackathon Phase 2 Backend",
  "version": "1.0.0",
  "environment": "development",
  "timestamp": "2026-01-17T09:31:54.489Z"
}
```

## Error Codes

| HTTP Status | Meaning |
|-------------|---------|
| 200 | Success for GET, PUT, DELETE operations |
| 201 | Created for successful POST operations |
| 400 | Bad Request - invalid input |
| 401 | Unauthorized - authentication required |
| 404 | Not Found - resource does not exist |
| 409 | Conflict - resource already exists |
| 500 | Internal Server Error |

## Rate Limiting
No explicit rate limiting is implemented in this version. Consider adding if needed for production use.

## Security Headers
The API includes appropriate security headers including CORS configuration for frontend integration.