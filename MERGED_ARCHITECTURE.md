# Multi-Phase Todo Application

This repository contains a complete, multi-phase todo application with AI capabilities. All phases are organized in a unified structure:

## Phase Structure

### Phase 2: Core Application
- **Backend**: Node.js/TypeScript/Express with JWT authentication and PostgreSQL
- **Frontend**: Next.js frontend with responsive UI
- **Location**: `./phase2/`

### Phase 3: AI Chatbot
- **Backend**: Python/FastAPI with Cohere AI integration
- **Frontend**: React chat interface
- **Location**: `./phase3/`

### Phase 4: Deployment
- **Containerization**: Docker files for all services
- **Orchestration**: Kubernetes configurations
- **Automation**: Deployment scripts
- **Location**: `./phase-4/`

## Unified Architecture

```
├── phase2/                 # Core application (Node.js/TS/Express + Next.js)
│   ├── backend/            # Node.js/TypeScript/Express backend
│   └── frontend/           # Next.js frontend
├── phase3/                 # AI Chatbot (Python/FastAPI)
│   ├── backend/            # Python FastAPI application with Cohere AI
│   └── frontend/           # React chat interface
├── phase-4/                # Deployment (Docker/Kubernetes)
│   ├── docker/             # Dockerfiles for all services
│   ├── k8s/                # Kubernetes configurations
│   ├── env/                # Environment configuration
│   └── scripts/            # Deployment scripts
├── README.md               # This file
├── CONSTITUTION.md         # Project governance document
└── PROJECT_SUMMARY.md      # Comprehensive project documentation
```

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
# Build and deploy
cd phase-4
./scripts/build-images.sh
./scripts/deploy-minikube.sh
```

## API Integration

- Phase 2 provides the core authentication and task management APIs
- Phase 3 provides AI processing and natural language understanding
- Both phases work together to provide a complete AI-powered task management system
- Phase 4 provides containerized deployment for all services

## Security

- JWT-based authentication across all services
- User data isolation
- Secure API communication
- Environment variable management for secrets