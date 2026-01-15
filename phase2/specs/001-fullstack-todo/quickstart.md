# Quickstart Guide: AI Skills Layer for Todo Application

**Date**: 2026-01-09
**Feature**: AI Skills Preview
**Prerequisites**: Phase-2 backend deployed and running

## Overview

This guide provides quick setup instructions for the AI Skills layer that enables natural language processing for the Todo application. The AI layer sits between user input and existing Phase-2 APIs.

## Architecture Overview

```
User Chat Input
  ↓
AI Skills Layer (Intent Detection + Skill Routing)
  ↓
Phase-2 Backend APIs (existing functionality)
  ↓
Database (existing models)
```

## Prerequisites

- Phase-2 backend must be running and accessible
- JWT authentication must be working
- Python 3.10+ installed
- FastAPI application running on standard port (8000)

## Setup Steps

### 1. Verify Backend is Running

First, ensure your Phase-2 backend is running:

```bash
cd backend
python main.py
# Backend should be available at http://localhost:8000
```

### 2. Install Dependencies

The AI Skills layer uses the same dependencies as the backend:

```bash
pip install -r requirements.txt
```

### 3. Verify AI Skills Integration

The AI Skills are already integrated into the main application. Check that the routes are available:

- `/api/ai/process` - Process natural language requests
- `/api/ai/skills` - Get list of available skills

## Usage Examples

### Testing the AI Skills

#### 1. Process Natural Language Request

```bash
curl -X POST http://localhost:8000/api/ai/process \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"input": "Add buy milk"}'
```

#### 2. List Available Skills

```bash
curl -X GET http://localhost:8000/api/ai/skills \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Supported Natural Language Patterns

#### Create Task Skills
- "Add buy milk"
- "Create task finish report"
- "New task call mom"
- "Task buy groceries"

#### List Tasks Skills
- "Show my tasks"
- "List my tasks"
- "View my tasks"
- "What tasks do I have?"

#### Complete Task Skills
- "Complete buy milk"
- "Finish report task"
- "Mark grocery shopping done"
- "Check finish report"

## Configuration

### Environment Variables

The AI Skills layer uses the same configuration as the existing backend:

```bash
# In backend/.env
DATABASE_URL=sqlite:///./todo.db
JWT_SECRET=your-super-secret-jwt-key-here
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
API_HOST=0.0.0.0
API_PORT=8000
```

### Base URL Configuration

The AI Skills layer automatically uses the existing API base URL. No additional configuration required.

## API Endpoints

### AI Processing Endpoint
- **URL**: `POST /api/ai/process`
- **Auth**: JWT Bearer token required
- **Request**: `{"input": "natural language text"}`
- **Response**: Standard SuccessResponse format

### Skills Discovery Endpoint
- **URL**: `GET /api/ai/skills`
- **Auth**: JWT Bearer token required
- **Response**: Array of available skills with examples

## Development

### Running in Development Mode

```bash
cd backend
python main.py
# Visit http://localhost:8000/api/docs for API documentation
# AI skills endpoints will be available under "ai-skills" section
```

### Testing Skills Implementation

The skills are implemented in `backend/skills/todo_skills.py`:

```python
# Example skill implementation
def process_request(self, user_input: str, user_id: UUID, jwt_token: str = None):
    # Natural language processing
    # Intent detection
    # API call forwarding
    # Response formatting
```

## Security Considerations

### JWT Token Handling
- Tokens are forwarded unchanged to existing APIs
- User isolation is maintained by existing backend logic
- No additional authentication layer added

### Input Validation
- Natural language input is validated for length
- Skill execution is limited to existing API endpoints
- All existing security measures remain in place

## Troubleshooting

### Common Issues

1. **401 Unauthorized**: Ensure JWT token is valid and properly formatted
2. **404 Not Found**: Verify the `/api/ai/` endpoints are registered
3. **500 Server Error**: Check backend logs for specific error details

### Debugging Tips

1. Enable debug mode in backend configuration
2. Check that existing Phase-2 APIs are working
3. Verify JWT token is valid by testing other endpoints
4. Review logs for intent detection patterns

## Next Steps

1. **Integration Testing**: Test AI skills with real user workflows
2. **Performance Testing**: Validate response times under load
3. **Pattern Expansion**: Add more natural language patterns
4. **Error Handling**: Enhance error responses for better UX

## Architecture Notes

- The AI Skills layer is optional and doesn't affect Phase-2 functionality
- All existing APIs continue to work normally
- Skills layer adds a new endpoint category without modifying existing code
- Security model remains unchanged

## Support

For issues with the AI Skills layer:
- Check existing Phase-2 backend functionality first
- Verify JWT authentication is working
- Review logs in the backend application
- Ensure all dependencies are properly installed

## Document Versioning

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-09 | Initial quickstart guide for AI Skills Layer |