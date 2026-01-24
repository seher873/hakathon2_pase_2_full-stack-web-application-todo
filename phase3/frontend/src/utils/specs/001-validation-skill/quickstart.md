# Quickstart Guide: Phase-III AI Layer for Todo Application

## Prerequisites
- Node.js 24.12.0 or higher
- TypeScript 5.3.3
- PostgreSQL database (with Neon connection)
- Phase-2 backend API running and accessible
- Valid JWT authentication tokens

## Setup Instructions

### 1. Clone and Navigate
```bash
cd phase3
npm install
```

### 2. Environment Configuration
Create a `.env` file with the following variables:
```env
JWT_SECRET=your_jwt_secret_key
BACKEND_API_URL=http://localhost:3000/api
DATABASE_URL=postgresql://username:password@neon-host.region.aws.neon.tech/dbname
PORT=4000
```

### 3. Initialize the AI Layer
```bash
npm run build
npm start
```

## Running Tests
```bash
# Unit tests
npm run test:unit

# Integration tests
npm run test:integration

# Contract tests
npm run test:contract
```

## Basic Usage

### Starting the Service
```bash
npm start
# Server will start on http://localhost:4000
```

### Making Requests
```bash
# Example request with natural language command
curl -X POST http://localhost:4000/api/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"command": "Add buy groceries to my tasks"}'
```

## Key Endpoints

### AI Chat Endpoint
- **POST** `/api/chat`
- **Headers**: Authorization: Bearer [JWT_TOKEN]
- **Request Body**: `{"command": "natural language command"}`
- **Response**: Processed intent and result from skill execution

### Health Check
- **GET** `/health`
- **Response**: Service status and dependencies

## Development Workflow

### Adding New Skills
1. Create new skill in `/skills/` directory
2. Define input/output schemas
3. Register skill with orchestrator
4. Add corresponding tests

### Extending Intent Recognition
1. Update regex patterns in Intent Agent
2. Add new action types to Intent Object schema
3. Create corresponding skill handlers
4. Test with sample commands

## Troubleshooting

### Common Issues
- **JWT Token Required**: Ensure Authorization header is properly formatted
- **Backend Unreachable**: Verify BACKEND_API_URL is correct and accessible
- **Intent Not Recognized**: Check command format matches defined patterns

### Logs
- Service logs are written to `logs/app.log`
- Error logs are written to `logs/error.log`
- Debug logs available with `DEBUG=true` environment variable
