# Complete Multi-Phase Todo Application

## Project Overview

This is a comprehensive, multi-phase todo application that combines a modern frontend, robust backend, and AI-powered chatbot interface. The project follows a spec-driven development approach with 5 distinct phases.

## Architecture Overview

```
├── phase2/                 # Phase 2: Core application (Node.js/TS/Express + Next.js)
│   ├── backend/            # Node.js/TypeScript/Express backend
│   │   ├── src/
│   │   │   ├── server.ts              # Main application entry point
│   │   │   ├── services/
│   │   │   │   └── database.ts        # PostgreSQL connection pool
│   │   │   ├── middleware/
│   │   │   │   └── auth.ts            # JWT authentication middleware
│   │   │   ├── routes/
│   │   │   │   ├── auth.ts            # Authentication endpoints
│   │   │   │   ├── tasks.ts           # Task management endpoints
│   │   │   │   ├── health.ts          # Health check endpoints
│   │   │   │   └── ai.ts              # AI processing endpoints
│   │   │   └── init-db.ts             # Database initialization script
│   │   ├── package.json               # Dependencies and scripts
│   │   ├── tsconfig.json              # TypeScript configuration
│   │   └── .env                       # Environment variables
│   └── frontend/           # Next.js frontend
│       ├── src/
│       │   ├── app/          # Next.js app router pages
│       │   ├── components/   # Reusable UI components
│       │   ├── hooks/        # Custom React hooks
│       │   ├── lib/          # Utilities and libraries
│       │   ├── services/     # API service clients
│       │   ├── types/        # TypeScript type definitions
│       │   └── utils/        # Utility functions
│       ├── public/
│       ├── package.json
│       └── next.config.js
├── phase3/                 # Phase 3: AI Chatbot (Python/FastAPI)
│   ├── backend/            # Python FastAPI application with Cohere AI
│   │   ├── main.py         # Application entry point
│   │   ├── requirements.txt
│   │   └── src/
│   │       ├── api/
│   │       │   ├── auth.py
│   │       │   ├── tasks.py
│   │       │   ├── health.py
│   │       │   ├── chatbot.py
│   │       │   └── ai.py
│   │       └── services/
│   │           ├── chatbot_service.py
│   │           ├── conversation_service.py
│   │           └── database.py
│   └── frontend/           # React chat interface
├── phase-4/                # Phase 4: Deployment (Docker/Kubernetes)
│   ├── docker/
│   │   ├── backend.Dockerfile        # Phase-2 backend container
│   │   ├── chatbot.Dockerfile        # Phase-3 AI chatbot container
│   │   └── frontend.Dockerfile       # Phase-2 frontend container
│   ├── k8s/
│   │   ├── backend-deployment.yaml
│   │   ├── backend-service.yaml
│   │   ├── chatbot-deployment.yaml
│   │   ├── chatbot-service.yaml
│   │   ├── frontend-deployment.yaml
│   │   └── frontend-service.yaml
│   ├── env/
│   │   ├── backend.env.example
│   │   ├── chatbot.env.example
│   │   └── frontend.env.example
│   ├── scripts/
│   │   ├── build-images.sh
│   │   ├── push-images.sh
│   │   └── deploy-minikube.sh
│   └── README.md
├── README.md              # Project overview
├── CONSTITUTION.md        # Project governance document
└── ...
```

## Phase Details

### Phase 2: Core Application (Completed)
**Technology Stack**: Node.js/TypeScript/Express backend with Next.js frontend

**Backend Features**:
- JWT-based authentication (register, login, logout, me)
- Task CRUD operations (create, read, update, delete)
- PostgreSQL database with Neon integration
- Health checks and proper error handling
- CORS configured for frontend integration

**Key Files**:
- `phase2/backend/src/server.ts` - Main server with enhanced CORS and response handling
- `phase2/backend/src/routes/ai/index.ts` - AI processing endpoints
- `phase2/backend/src/middleware/auth.ts` - JWT authentication middleware
- `phase2/backend/src/services/database.ts` - PostgreSQL connection pool

### Phase 3: AI Chatbot (Completed)
**Technology Stack**: Python/FastAPI with Cohere AI integration

**Features**:
- Natural language processing for task management
- Intent classification (create/list/update/delete tasks)
- Conversation history tracking
- Integration with Phase-2 backend APIs

**Key Files**:
- `phase3/backend/main.py` - FastAPI application entry point
- `phase3/backend/src/api/ai.py` - AI processing endpoints
- `phase3/backend/src/services/chatbot_service.py` - Core AI service with Cohere integration

### Phase 4: Deployment (Completed)
**Technology Stack**: Docker containers with Kubernetes orchestration

**Features**:
- Containerized services for all components
- Kubernetes deployments and services
- Environment configuration management
- Deployment scripts for local and production

## How the Phases Work Together

### 1. User Authentication Flow
1. User registers/logs in via Phase-2 backend (Node.js/Express)
2. JWT token is issued and stored in frontend
3. Token is used to authenticate requests to both Phase-2 and Phase-3 APIs

### 2. Task Management Flow
1. Standard task operations (CRUD) go through Phase-2 backend
2. AI-powered task operations go through Phase-3 chatbot
3. Phase-3 chatbot can call Phase-2 backend APIs to perform actual operations

### 3. AI Processing Flow
1. User sends natural language command to Phase-3 chatbot API
2. Chatbot service classifies intent using Cohere AI
3. Based on intent, chatbot may call Phase-2 backend APIs to perform operations
4. Response is returned to frontend

## API Endpoints

### Phase-2 Backend (Node.js/Express)
- `GET /api/health` - Health check
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user
- `GET /api/tasks` - Get user tasks
- `POST /api/tasks` - Create task
- `PUT /api/tasks/:id` - Update task
- `DELETE /api/tasks/:id` - Delete task
- `POST /api/ai/process` - AI command processing

### Phase-3 Backend (Python/FastAPI)
- `GET /api/health` - Health check
- `POST /api/chatbot/chat` - Chat with AI
- `POST /api/ai/process` - AI command processing

## Security Features

1. **JWT Authentication**: All APIs require valid JWT tokens
2. **User Isolation**: Users can only access their own data
3. **Input Validation**: All user inputs are validated
4. **Environment Security**: Secrets are stored in environment variables
5. **CORS Protection**: Proper CORS configuration prevents unauthorized access

## Deployment Architecture

The application is deployed as 3 separate services:
1. **Backend Service** (Phase-2): Handles authentication and task management
2. **Chatbot Service** (Phase-3): Handles AI processing and natural language understanding
3. **Frontend Service**: Serves the user interface

All services are containerized with Docker and orchestrated with Kubernetes.

## Environment Variables

### Phase-2 Backend
- `DATABASE_URL` - PostgreSQL database connection string
- `JWT_SECRET` - Secret key for JWT token signing
- `API_PORT` - Port for the backend service

### Phase-3 Backend
- `COHERE_API_KEY` - API key for Cohere AI service
- `JWT_SECRET_KEY` - Secret key for JWT token verification (should match Phase-2)
- `BACKEND_BASE_URL` - URL of the Phase-2 backend for API calls
- `PORT` - Port for the chatbot service

## Running the Application

### Local Development
1. Start Phase-2 backend:
   ```bash
   cd phase2/backend
   npm install
   npm run dev
   ```

2. Start Phase-2 frontend:
   ```bash
   cd phase2/frontend
   npm install
   npm run dev
   ```

3. Start Phase-3 chatbot:
   ```bash
   cd phase3/backend
   pip install -r requirements.txt
   python main.py
   ```

### Containerized Deployment
1. Build Docker images:
   ```bash
   cd phase-4
   ./scripts/build-images.sh
   ```

2. Deploy to Kubernetes:
   ```bash
   ./scripts/deploy-minikube.sh
   ```

## Project Constitution

This project follows the ROOT AI CONSTITUTION which defines:
- Spec-Driven Development methodology
- Safety and determinism requirements
- User isolation principles
- Explainability and observability standards
- Phase-based development approach

## Success Criteria Achieved

✓ Stable task management functionality
✓ Responsive and beautiful UI
✓ Proper authentication and data security
✓ Comprehensive API coverage
✓ Production-ready Node.js/TypeScript/Express backend
✓ Secure JWT authentication system
✓ PostgreSQL integration with Neon database
✓ AI-powered natural language interface
✓ Containerized deployment with Kubernetes
✓ Complete documentation and deployment guides