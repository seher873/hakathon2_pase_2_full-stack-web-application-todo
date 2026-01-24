# API Contract: AI Chatbot Service

## Overview
This document specifies the API contracts for the AI Chatbot service in Phase-3, defining endpoints, request/response formats, and error handling.

## Base URL
```
https://your-domain.com/api/chatbot
```

## Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer {jwt_token}
```

## Endpoints

### 1. Send Message
Send a message to the AI chatbot and receive a response.

**Endpoint**: `POST /message`

**Request Headers**:
- `Authorization: Bearer {token}`
- `Content-Type: application/json`

**Request Body**:
```json
{
  "message": "string (required) - The message content to send to the chatbot",
  "conversationId": "string (optional, UUID) - ID of existing conversation to continue, or null for new conversation"
}
```

**Response Codes**:
- `200 OK` - Message processed successfully
- `400 Bad Request` - Invalid request format or missing required fields
- `401 Unauthorized` - Invalid or missing authentication token
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - AI service or system error

**Success Response (200)**:
```json
{
  "success": true,
  "data": {
    "conversationId": "string (UUID) - ID of the conversation",
    "messageId": "string (UUID) - ID of the sent message",
    "response": "string - AI-generated response to the message",
    "timestamp": "string (ISO 8601) - Timestamp of the response",
    "usage": {
      "promptTokens": "integer - Number of tokens in the input message",
      "completionTokens": "integer - Number of tokens in the AI response",
      "totalTokens": "integer - Total tokens used"
    }
  }
}
```

**Error Response**:
```json
{
  "success": false,
  "error": {
    "code": "string - Error code (e.g., 'INVALID_INPUT', 'AUTH_FAILED', 'RATE_LIMIT_EXCEEDED')",
    "message": "string - Human-readable error message",
    "details": "object (optional) - Additional error details"
  }
}
```

### 2. Get Conversation History
Retrieve a list of user's conversations with pagination.

**Endpoint**: `GET /conversations`

**Query Parameters**:
- `page` (optional, integer, default: 1) - Page number for pagination
- `limit` (optional, integer, default: 20, max: 50) - Number of conversations per page
- `sort` (optional, string, default: 'updatedAt') - Sort field ('createdAt', 'updatedAt')
- `order` (optional, string, default: 'desc') - Sort order ('asc', 'desc')

**Response Codes**:
- `200 OK` - Conversations retrieved successfully
- `401 Unauthorized` - Invalid or missing authentication token
- `400 Bad Request` - Invalid query parameters

**Success Response (200)**:
```json
{
  "success": true,
  "data": {
    "conversations": [
      {
        "id": "string (UUID) - Conversation ID",
        "title": "string - Conversation title",
        "createdAt": "string (ISO 8601) - Creation timestamp",
        "updatedAt": "string (ISO 8601) - Last activity timestamp",
        "messageCount": "integer - Number of messages in the conversation"
      }
    ],
    "pagination": {
      "page": "integer - Current page number",
      "limit": "integer - Number of items per page",
      "total": "integer - Total number of conversations",
      "pages": "integer - Total number of pages"
    }
  }
}
```

### 3. Get Specific Conversation
Retrieve a specific conversation with all its messages.

**Endpoint**: `GET /conversation/{id}`

**Path Parameters**:
- `id` (string, required, UUID) - The conversation ID

**Response Codes**:
- `200 OK` - Conversation retrieved successfully
- `401 Unauthorized` - Invalid or missing authentication token
- `404 Not Found` - Conversation not found or doesn't belong to user
- `400 Bad Request` - Invalid conversation ID format

**Success Response (200)**:
```json
{
  "success": true,
  "data": {
    "conversation": {
      "id": "string (UUID) - Conversation ID",
      "title": "string - Conversation title",
      "createdAt": "string (ISO 8601) - Creation timestamp",
      "updatedAt": "string (ISO 8601) - Last activity timestamp",
      "messages": [
        {
          "id": "string (UUID) - Message ID",
          "senderType": "string ('user' or 'ai') - Who sent the message",
          "content": "string - Message content",
          "timestamp": "string (ISO 8601) - When the message was sent"
        }
      ]
    }
  }
}
```

### 4. Create New Conversation
Start a new conversation with the AI chatbot.

**Endpoint**: `POST /conversation`

**Request Headers**:
- `Authorization: Bearer {token}`
- `Content-Type: application/json`

**Request Body**:
```json
{
  "title": "string (optional) - Initial title for the conversation, auto-generated if not provided"
}
```

**Response Codes**:
- `201 Created` - Conversation created successfully
- `401 Unauthorized` - Invalid or missing authentication token
- `400 Bad Request` - Invalid request format

**Success Response (201)**:
```json
{
  "success": true,
  "data": {
    "conversation": {
      "id": "string (UUID) - New conversation ID",
      "title": "string - Conversation title",
      "createdAt": "string (ISO 8601) - Creation timestamp",
      "updatedAt": "string (ISO 8601) - Last activity timestamp"
    }
  }
}
```

### 5. Update Conversation
Update conversation properties (e.g., title).

**Endpoint**: `PUT /conversation/{id}`

**Path Parameters**:
- `id` (string, required, UUID) - The conversation ID

**Request Headers**:
- `Authorization: Bearer {token}`
- `Content-Type: application/json`

**Request Body**:
```json
{
  "title": "string (required) - New title for the conversation"
}
```

**Response Codes**:
- `200 OK` - Conversation updated successfully
- `401 Unauthorized` - Invalid or missing authentication token
- `404 Not Found` - Conversation not found or doesn't belong to user
- `400 Bad Request` - Invalid request format

**Success Response (200)**:
```json
{
  "success": true,
  "data": {
    "conversation": {
      "id": "string (UUID) - Conversation ID",
      "title": "string - Updated conversation title",
      "createdAt": "string (ISO 8601) - Creation timestamp",
      "updatedAt": "string (ISO 8601) - Last activity timestamp"
    }
  }
}
```

### 6. Delete Conversation
Archive or delete a conversation.

**Endpoint**: `DELETE /conversation/{id}`

**Path Parameters**:
- `id` (string, required, UUID) - The conversation ID

**Response Codes**:
- `200 OK` - Conversation deleted successfully
- `401 Unauthorized` - Invalid or missing authentication token
- `404 Not Found` - Conversation not found or doesn't belong to user
- `400 Bad Request` - Invalid conversation ID format

**Success Response (200)**:
```json
{
  "success": true,
  "data": {
    "message": "string - Confirmation message"
  }
}
```

### 7. Get User Session Info
Get information about the current user session related to chatbot.

**Endpoint**: `GET /session`

**Response Codes**:
- `200 OK` - Session info retrieved successfully
- `401 Unauthorized` - Invalid or missing authentication token

**Success Response (200)**:
```json
{
  "success": true,
  "data": {
    "session": {
      "userId": "string (UUID) - User ID",
      "activeConversationId": "string (UUID, nullable) - Currently active conversation ID",
      "lastActiveAt": "string (ISO 8601) - Last activity timestamp",
      "rateLimitInfo": {
        "remaining": "integer - Remaining requests in current window",
        "resetTime": "string (ISO 8601) - When the rate limit resets"
      }
    }
  }
}
```

## Error Codes

| Code | Description |
|------|-------------|
| `AUTH_FAILED` | Authentication token is invalid or expired |
| `INVALID_INPUT` | Request body or parameters are malformed |
| `RESOURCE_NOT_FOUND` | Requested resource (conversation, etc.) does not exist |
| `RATE_LIMIT_EXCEEDED` | User has exceeded the allowed request rate |
| `AI_SERVICE_ERROR` | The AI service is temporarily unavailable |
| `VALIDATION_ERROR` | Request failed validation checks |
| `INTERNAL_ERROR` | An unexpected server error occurred |

## Rate Limiting
All authenticated users are subject to rate limiting:
- 10 requests per minute per user
- Count resets every 60 seconds
- Expressed in the response headers and session info

## Webhook Events (Future Extension)
The system may support webhook events for real-time notifications:
- `conversation.created` - When a new conversation is started
- `message.received` - When a message is received from the AI
- `conversation.archived` - When a conversation is archived

These events would be sent to a configured webhook URL with signatures for verification.