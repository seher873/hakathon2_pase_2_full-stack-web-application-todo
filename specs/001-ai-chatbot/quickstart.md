# Quickstart Guide: AI Chatbot for Phase-3

## Overview
This guide provides a quick setup and run instructions for the AI Chatbot feature in Phase-3.

## Prerequisites
- Node.js 20.x or higher
- PostgreSQL database (with Neon DB connection details)
- OpenAI API key (or equivalent AI service key)
- Existing Phase-2 backend running and accessible

## Setup Instructions

### 1. Clone and Navigate
```bash
# Ensure you're in the hakathon_2 project root
cd /path/to/hakathon_2
git checkout 001-ai-chatbot  # Switch to the feature branch
```

### 2. Backend Setup
```bash
# Navigate to the Phase-3 backend
cd phase3/backend

# Install dependencies
npm install

# Copy environment template and configure
cp .env.example .env
# Edit .env with your database and AI service credentials
```

#### Environment Variables
```bash
# Database Configuration (from Phase-2)
DB_HOST=your_neon_db_host
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
DATABASE_URL=your_postgres_connection_string

# AI Service Configuration
OPENAI_API_KEY=your_openai_api_key  # Or equivalent for your chosen AI service
AI_MODEL_NAME=gpt-4-turbo  # Or equivalent for your chosen AI service

# JWT Configuration (from Phase-2)
JWT_SECRET=your_jwt_secret
JWT_EXPIRES_IN=24h

# Rate Limiting
RATE_LIMIT_WINDOW_MS=60000  # 1 minute window
RATE_LIMIT_MAX_REQUESTS=10  # Max 10 requests per window
```

### 3. Database Setup
```bash
# Run migrations to create chatbot-related tables
npm run migrate

# Verify database connectivity
npm run db:health-check
```

### 4. Frontend Setup
```bash
# Navigate to the Phase-3 frontend
cd ../frontend

# Install dependencies
npm install

# The frontend will use the same environment as the Phase-2 frontend
# Ensure your backend API endpoints are properly configured
```

## Running the Application

### 1. Start Backend Services
```bash
# From phase3/backend directory
npm run dev
# The backend will start on port 3001 (or configured port)
```

### 2. Start Frontend
```bash
# From phase3/frontend directory
npm run dev
# The frontend will start on port 3000 (or configured port)
```

### 3. Access the Chatbot
Open your browser and navigate to:
- Frontend: `http://localhost:3000/chat`
- API endpoints: `http://localhost:3001/api/chatbot`

## API Endpoints

### Chat Functionality
- `POST /api/chatbot/message` - Send a message to the chatbot
- `GET /api/chatbot/conversations` - Get user's conversation history
- `GET /api/chatbot/conversation/:id` - Get specific conversation with messages
- `DELETE /api/chatbot/conversation/:id` - Archive/delete a conversation

### Request Format
```json
{
  "message": "Your message to the chatbot",
  "conversationId": "optional - UUID if continuing existing conversation"
}
```

### Response Format
```json
{
  "success": true,
  "data": {
    "conversationId": "UUID of the conversation",
    "response": "AI-generated response",
    "timestamp": "ISO timestamp"
  }
}
```

## Testing

### Unit Tests
```bash
# Backend unit tests
cd phase3/backend
npm run test:unit

# Frontend unit tests
cd phase3/frontend
npm run test:unit
```

### Integration Tests
```bash
# Backend integration tests
cd phase3/backend
npm run test:integration

# End-to-end tests
cd phase3/frontend
npm run test:e2e
```

## Troubleshooting

### Common Issues
1. **Database Connection Errors**: Verify your PostgreSQL credentials in `.env`
2. **AI Service Errors**: Check your API key and ensure the service is accessible
3. **Authentication Issues**: Ensure JWT configuration matches Phase-2 settings
4. **CORS Errors**: Verify frontend and backend ports match your configuration

### Logs
- Backend logs: Check console output when running `npm run dev`
- Frontend logs: Check browser console and console output when running `npm run dev`

## Next Steps
1. Explore the API documentation at `/api/docs` (if available)
2. Review the full implementation plan in `specs/001-ai-chatbot/plan.md`
3. Check the data model in `specs/001-ai-chatbot/data-model.md`
4. Look at the task breakdown in `specs/001-ai-chatbot/tasks.md` (after running `/sp.tasks`)