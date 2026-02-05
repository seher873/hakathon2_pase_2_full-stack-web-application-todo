# Phase-4: Docker Development Setup

This setup provides a Docker-based development environment with volume mounts for live reloading during development.

## Services

- **Backend**: Runs on port 8000
- **Chatbot**: Runs on port 9000
- **Frontend**: Runs on port 3000

## Prerequisites

- Docker Engine (v20+) and Docker Compose (v2+) OR
- Node.js 20, Python 3.11, and required dependencies

## How to Run

### Option 1: Using Docker (Recommended)
1. Navigate to the phase-4 directory:
   ```bash
   cd /path/to/hakathon_2/phase-4
   ```

2. Start the development environment:
   ```bash
   docker compose -f docker-compose.dev.yml up --build
   ```

3. To run in detached mode:
   ```bash
   docker compose -f docker-compose.dev.yml up --build -d
   ```

4. To stop the development environment:
   ```bash
   docker compose -f docker-compose.dev.yml down
   ```

### Option 2: Manual Setup (Alternative)
If Docker is not available or not working, you can set up the development environment manually:

1. Run the setup script:
   ```bash
   chmod +x setup-dev-env.sh
   ./setup-dev-env.sh
   ```

2. Start each service individually:
   - Backend: `cd ../phase2/backend && npm install && npm run dev`
   - Chatbot: `cd ../phase3/backend && pip install -r requirements.txt && python3 -m uvicorn main:app --reload --port 9000`
   - Frontend: `cd ../phase2/frontend && npm install && npm run dev`

## Features

- Volume mounts for live code reloading (Docker option)
- Isolated development environment (Docker option)
- Proper service dependencies
- Hot reloading enabled for all services

## Troubleshooting

### Docker Issues
- If you encounter Docker bus errors, ensure Docker Desktop is running properly
- Check that you have sufficient disk space and memory allocated to Docker
- For permission issues, make sure your project directory has proper read/write permissions
- For Node.js modules issues, try clearing the Docker volume cache:
  ```bash
  docker volume prune
  ```

### Manual Setup Issues
- Ensure Node.js 20+ is installed: `node --version`
- Ensure Python 3.11+ is installed: `python3 --version`
- Ensure pip is available: `pip3 --version`