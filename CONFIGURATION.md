# Multi-Phase Todo Application Configuration

This file provides unified configuration information for all phases of the application.

## Phase 2: Core Application
- Backend: Node.js/TypeScript/Express running on port 4000
- Frontend: Next.js running on port 3000
- Database: PostgreSQL (Neon) 
- Authentication: JWT-based

## Phase 3: AI Chatbot
- Backend: Python/FastAPI running on port 8000
- AI Service: Cohere API integration
- Connection: Interacts with Phase 2 backend APIs

## Phase 4: Deployment
- Containerization: Docker
- Orchestration: Kubernetes
- Services: backend, chatbot, frontend

## Environment Variables

### Phase 2 Backend (.env)
```
DATABASE_URL=postgresql://user:password@neon-hosted-db.tech:5432/backend_db
JWT_SECRET=your_jwt_secret_key_here
API_PORT=4000
NODE_ENV=development
```

### Phase 3 Backend (.env)
```
COHERE_API_KEY=your_cohere_api_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here  # Should match Phase 2
BACKEND_BASE_URL=http://localhost:4000
PORT=8000
DATABASE_URL=postgresql://user:password@neon-hosted-db.tech:5432/chatbot_db
```

### Phase 2 Frontend (.env)
```
NEXT_PUBLIC_BACKEND_BASE_URL=http://localhost:4000
NEXT_PUBLIC_CHATBOT_BASE_URL=http://localhost:8000
```

## API Endpoints

### Phase 2 Backend
- Health: GET `/api/health`
- Auth: POST `/api/auth/register`, POST `/api/auth/login`, GET `/api/auth/me`
- Tasks: GET `/api/tasks`, POST `/api/tasks`, PUT `/api/tasks/:id`, DELETE `/api/tasks/:id`
- AI: POST `/api/ai/process`

### Phase 3 Backend
- Health: GET `/api/health`
- Chatbot: POST `/api/chatbot/chat`
- AI: POST `/api/ai/process`

## Development Workflow

1. Start Phase 2 backend: `npm run phase2:backend:start`
2. Start Phase 2 frontend: `npm run phase2:frontend:start`
3. Start Phase 3 backend: `npm run phase3:backend:start`
4. Access the application at http://localhost:3000

## Deployment Workflow

1. Build Docker images: `npm run phase4:build`
2. Deploy to Kubernetes: `npm run phase4:deploy`