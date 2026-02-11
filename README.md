# Multi-Phase Todo Application with AI Integration

This repository contains a complete, multi-phase todo application with AI capabilities. The project follows a spec-driven, multi-phase approach to building a task management application with advanced AI features.

## Unified Architecture

```
├── phase2/                 # Phase 2: Core application (Node.js/TS/Express + Next.js)
│   ├── backend/            # Node.js/TypeScript/Express backend
│   └── frontend/           # Next.js frontend
├── phase3/                 # Phase 3: AI Chatbot (Python/FastAPI)
│   ├── backend/            # Python FastAPI application with Cohere AI
│   └── frontend/           # React chat interface
├── phase-4/                # Phase 4: Deployment (Docker/Kubernetes)
│   ├── docker/             # Dockerfiles for all services
│   ├── k8s/                # Kubernetes configurations
│   ├── env/                # Environment configuration
│   └── scripts/            # Deployment scripts
├── README.md               # This file
├── CONSTITUTION.md         # Project governance document
├── PROJECT_SUMMARY.md      # Comprehensive project documentation
└── MERGED_ARCHITECTURE.md  # Unified architecture documentation
```

## Phase Details

### Phase 2: Core Application (Completed)
- **Technology**: Node.js/TypeScript/Express backend with Next.js frontend
- **Features**:
  - JWT-based authentication (register, login, logout, me)
  - Task CRUD operations (create, read, update, delete)
  - PostgreSQL database with Neon integration
  - Health checks and proper error handling
  - CORS configured for frontend integration
- **Location**: `./phase2/`

### Phase 3: AI Chatbot (Completed)
- **Technology**: Python/FastAPI with Cohere AI integration
- **Features**:
  - Natural language processing for task management
  - Intent classification (create/list/update/delete tasks)
  - Conversation history tracking
  - Integration with Phase-2 backend APIs
- **Location**: `./phase3/`

### Phase 4: Deployment (Completed)
- **Technology**: Docker containers with Kubernetes orchestration
- **Features**:
  - Containerized services for all components
  - Kubernetes deployments and services
  - Environment configuration management
  - Deployment scripts for local and production
- **Location**: `./phase-4/`

## How to Run

### Phase 2 (Core Application)
```bash
# Backend
cd phase2/backend
npm install
npm run dev

# Frontend
cd phase2/frontend
npm install
npm run dev
```

### Phase 3 (AI Chatbot)
```bash
# Backend
cd phase3/backend
pip install -r requirements.txt
python main.py
```

### Phase 4 (Deployment)
```bash
# Build and deploy with Docker Compose (Recommended for local development)
docker-compose up --build

# Or build and deploy with Kubernetes (Production)
cd phase-4
./scripts/build-images.sh
./scripts/deploy-minikube.sh
```

## Database Configuration
- **Development**: SQLite is allowed (default for local development)
- **Production**: PostgreSQL with Neon is required (as documented in phase2/backend/.env.example)
- **Environment Variable**: Use `USE_POSTGRES=true` and `DATABASE_URL=postgresql://...` for production environments

## API Integration

- Phase 2 provides the core authentication and task management APIs
- Phase 3 provides AI processing and natural language understanding
- Both phases work together to provide a complete AI-powered task management system
- Phase 4 provides containerized deployment for all services

## Project Constitution

This project follows the ROOT AI CONSTITUTION which defines:
- Spec-Driven Development methodology
- Safety and determinism requirements
- User isolation principles
- Explainability and observability standards
- Phase-based development approach

For details, see `CONSTITUTION.md` in the root directory.

## Documentation

- `PROJECT_SUMMARY.md` - Comprehensive project documentation
- `MERGED_ARCHITECTURE.md` - Unified architecture overview
- `CONSTITUTION.md` - Project governance document
- Individual phase documentation in each phase directory
- Phase specifications in `./specs/` directory:
  - `specs/001-ai-chatbot/spec.md` - Phase 1: AI Chatbot specifications
  - `specs/002-core-app/spec.md` - Phase 2: Core application specifications
  - `specs/003-validation/spec.md` - Phase 3: Validation specifications
  - `specs/004-k8s-helm-deployment/spec.md` - Phase 4: Kubernetes deployment specifications

## Phase Specifications

Each phase of the project has detailed specifications:

### Phase 1: AI Chatbot
- **Location**: `./specs/001-ai-chatbot/spec.md`
- **Focus**: AI-powered task management interface
- **Technology**: Python/FastAPI with Cohere AI integration

### Phase 2: Core Application
- **Location**: `./specs/002-core-app/spec.md`
- **Focus**: Core task management application with authentication
- **Technology**: Node.js/TypeScript/Express backend with Next.js frontend

### Phase 3: Validation
- **Location**: `./specs/003-validation/spec.md`
- **Focus**: Validation and verification of AI behaviors
- **Technology**: Validation frameworks and testing protocols

### Phase 4: Kubernetes Deployment
- **Location**: `./specs/004-k8s-helm-deployment/spec.md`
- **Focus**: Containerized deployment with Helm charts
- **Components**: Dockerfiles, Helm charts, deployment configurations
- **Requirements**: Containerized services, environment-specific configurations