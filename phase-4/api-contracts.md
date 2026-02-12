# API Contracts: Phase-4 Docker Development Environment

## Overview
This document defines the API contracts for the services running in the Docker development environment. These contracts represent the interfaces between the frontend and backend services.

## Backend Service API Contract

### Base URL
`http://backend:8000` (within Docker network)
`http://localhost:8000` (from host)

### Endpoints

#### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and receive JWT token
- `POST /auth/logout` - Logout and invalidate session
- `GET /auth/me` - Get current user information

#### Task Management
- `GET /tasks` - Retrieve all tasks for authenticated user
- `POST /tasks` - Create a new task
- `PUT /tasks/{id}` - Update a specific task
- `DELETE /tasks/{id}` - Delete a specific task
- `PATCH /tasks/{id}/status` - Update task completion status

#### Health Check
- `GET /health` - Health check endpoint


## Frontend Service API Contract

### Base URL
`http://frontend:3000` (within Docker network)
`http://localhost:3000` (from host)

### Endpoints

#### Static Assets
- `GET /` - Serve main application page
- `GET /static/*` - Serve static assets (CSS, JS, images)

#### API Proxy
- `GET /api/*` - Proxy requests to backend service

## Inter-Service Communication

### Frontend-Backend Communication
The frontend communicates with the backend for task management:
- Authentication and user data
- Task CRUD operations
- Health status

## Common Headers
- `Authorization: Bearer {token}` - For authenticated requests
- `Content-Type: application/json` - For JSON payloads
- `X-Request-ID: {uuid}` - For request tracing

## Error Responses
All services return errors in the following format:
```json
{
  "error": "error message",
  "code": "error code",
  "timestamp": "ISO datetime"
}
```

## Status Codes
- `200 OK` - Successful request
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request format
- `401 Unauthorized` - Missing or invalid authentication
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource does not exist
- `500 Internal Server Error` - Server-side error