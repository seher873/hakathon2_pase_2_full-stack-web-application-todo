# Docker Build and Container Fixes

## Issues Fixed

### 1. Removed Python/FastAPI Chatbot Service
**Problem:** The project should be Node.js based, but there was a Python/FastAPI chatbot service
- **Files:** `docker/chatbot.dev.Dockerfile`, `docker-compose.dev.yml`
- **Action:** Removed chatbot service from docker-compose.dev.yml and deleted chatbot Dockerfiles
- **Reason:** Following Phase-4 requirements that project should be Node.js based only

### 2. Backend Port Mapping
**Problem:** Port mapping mismatch between host and container
- **File:** `docker-compose.dev.yml`
- **Service:** backend
- **Original:** `"4001:4001"`
- **Fixed to:** `"4001:8000"`
- **Reason:** The backend Dockerfile exposes port 8000, so the container port should be 8000

## Build Status

All services now build successfully:
- ✅ **backend** - Node.js service on port 4001 (mapped to container port 8000)
- ✅ **frontend** - Next.js service on port 3000

## How to Use

### Build all images:
```bash
cd phase-4
docker compose -f docker-compose.dev.yml build
```

### Start all services:
```bash
docker compose -f docker-compose.dev.yml up -d
```

### View running containers:
```bash
docker compose -f docker-compose.dev.yml ps
```

### View logs:
```bash
# All services
docker compose -f docker-compose.dev.yml logs -f

# Specific service
docker compose -f docker-compose.dev.yml logs -f backend
docker compose -f docker-compose.dev.yml logs -f chatbot
docker compose -f docker-compose.dev.yml logs -f frontend
```

### Stop all services:
```bash
docker compose -f docker-compose.dev.yml down
```

## Service URLs

Once containers are running:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:4001
- **Chatbot API:** http://localhost:9000

## Notes

- All services use volumes for hot-reloading during development
- The build context is the parent directory (`hakathon_2`), allowing access to phase2 and phase3 folders
- Frontend runs as non-root user (nextjs) for security
- Python chatbot uses multi-stage build for smaller image size
