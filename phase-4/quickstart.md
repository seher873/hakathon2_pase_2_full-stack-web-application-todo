# Quickstart Guide: Phase-4 Docker Development Environment

## Overview
This guide provides quick setup instructions for the Docker-based development environment with volume mounts for live debugging of the Phase-2 backend and Phase-3 AI chatbot/fullstack application.

## Prerequisites
- Docker Engine (v20+)
- Docker Compose (v2+)
- Node.js 20 (on host for development tools)
- Git

## Quick Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd hakathon_2
```

### 2. Navigate to Project Root
```bash
cd /path/to/hakathon_2
```

### 3. Start the Development Environment
```bash
docker-compose -f phase-4/docker-compose.dev.yml up
```

### 4. Access the Services
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **AI Chatbot**: http://localhost:9000

## Development Workflow

### With Live Reloading
1. Make changes to the source code in your IDE
2. Changes will be automatically synced to the containers via volume mounts
3. Services will reload automatically (if using hot-reload mechanisms)

### Stopping the Environment
```bash
# In a separate terminal
docker-compose -f phase-4/docker-compose.dev.yml down
```

### Running in Detached Mode
```bash
# Start in background
docker-compose -f phase-4/docker-compose.dev.yml up -d

# Stop background containers
docker-compose -f phase-4/docker-compose.dev.yml down
```

## Troubleshooting

### Common Issues
1. **Port Already in Use**: Ensure ports 3000, 8000, and 9000 are available
2. **Permission Errors**: Check file permissions on the project directory
3. **Module Issues**: If experiencing node_modules issues, try clearing Docker volumes:
   ```bash
   docker volume prune
   ```

### Verifying Setup
Check that all services are running:
```bash
docker ps
```

You should see three containers running:
- phase4-backend-dev
- phase4-chatbot-dev
- phase4-frontend-dev

## Service Details

### Backend Service
- Runs on port 8000
- Contains Phase-2 backend code
- Connects to external PostgreSQL database

### Chatbot Service
- Runs on port 9000
- Contains Phase-3 AI chatbot functionality
- Communicates with backend service

### Frontend Service
- Runs on port 3000
- Contains Phase-3 frontend application
- Connects to backend and chatbot services