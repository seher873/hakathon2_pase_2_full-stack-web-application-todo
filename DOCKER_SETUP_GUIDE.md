# Docker Setup Guide - Multi-Service Todo Application

## Overview
This guide explains the Docker setup for all three services:
1. **Frontend** - Next.js (Phase 2)
2. **Backend** - Node.js/TypeScript (Phase 2)  
3. **AI Chatbot** - Python/FastAPI (Phase 3)

## Completed Work

### 1. Dockerfiles Created

#### Frontend Dockerfile (`phase2/frontend/Dockerfile`)
- Multi-stage build using Node.js 20 Alpine
- Optimized for production with standalone output
- Creates non-root user for security
- Port: 3000

#### Backend Dockerfile (`phase2/backend/Dockerfile`)
- Multi-stage build using Node.js 20 Alpine
- Builds TypeScript to JavaScript
- Production-ready with minimal dependencies
- Port: 3001

#### Chatbot Dockerfile (`phase3/backend/Dockerfile`)
- Python 3.11 slim base image
- Installs dependencies from requirements.txt
- Port: 9000

### 2. Docker Compose Configuration (`docker-compose.yml`)

Located at: `C:\Users\user\Desktop\hakathon_2\docker-compose.yml`

**Services configured:**
- `frontend`: Next.js application
- `backend`: Node.js/TypeScript API
- `chatbot`: Python FastAPI AI service

**Networking:**
- Custom bridge network: `todo-network`
- Services can communicate using service names

**Volumes:**
- `backend-data`: Persists backend database
- `chatbot-data`: Persists chatbot data

### 3. Configuration Updates

- Modified `phase2/frontend/next.config.js` to enable `standalone` output mode for Docker
- Created `.dockerignore` files for each service to optimize build context

## Current Status

### ✅ Successfully Built
- **Backend Service**: Image built and ready to run

### ⚠️ Build Issues Encountered

#### Frontend
- Issue: Package dependency conflicts between Next.js 14 and React 19
- Resolution needed: Update package-lock.json or use `npm install --legacy-peer-deps`

#### Chatbot  
- Issue: Pip dependency resolution timeout when installing requirements
- Root cause: Network timeouts and complex dependency trees (aiohttp versions)
- Resolution needed: Simplify requirements or increase timeout

## How to Build and Run

### Option 1: Build All Services (Recommended after fixing issues)
```bash
cd C:\Users\user\Desktop\hakathon_2

# Build all images
docker compose build

# Start all services
docker compose up -d

# View logs
docker compose logs -f
```

###Option 2: Build Services Individually
```bash
cd C:\Users\user\Desktop\hakathon_2

# Build and start backend only (READY TO USE)
docker compose build backend
docker compose up -d backend

# Build frontend (after fixing dependencies)
docker compose build frontend
docker compose up -d frontend

# Build chatbot (after fixing pip timeout)
docker compose build chatbot
docker compose up -d chatbot
```

### Option 3: Manual Build (if compose has issues)
```bash
# Backend
cd C:\Users\user\Desktop\hakathon_2\phase2\backend
docker build -t todo-backend .
docker run -d -p 3001:3001 --name backend todo-backend

# Frontend
cd C:\Users\user\Desktop\hakathon_2\phase2\frontend
docker build -t todo-frontend .
docker run -d -p 3000:3000 --name frontend todo-frontend

# Chatbot
cd C:\Users\user\Desktop\hakathon_2\phase3\backend
docker build -t todo-chatbot .
docker run -d -p 9000:9000 --name chatbot todo-chatbot
```

## Resolving Build Issues

### Frontend Dependency Issue
```bash
cd phase2/frontend

# Option 1: Update lock file
npm install

# Option 2: Use legacy peer deps (temporary)
# This is already configured in the Dockerfile

# Rebuild
docker compose build frontend
```

### Chatbot Timeout Issue
```bash
cd phase3/backend

# Option 1: Increase pip timeout
# Edit Dockerfile, change line:
RUN pip install --no-cache-dir --timeout=300 -r requirements.txt

# Option 2: Pin aiohttp version in requirements.txt
# Edit requirements.txt, change cohere line to:
cohere==4.8.0
aiohttp==3.9.5  # Add this line to pin version

# Rebuild
docker compose build chatbot
```

## Environment Variables

Create `.env` file in project root (optional):
```env
# AI API Keys (for chatbot functionality)
COHERE_API_KEY=your_cohere_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

## Accessing Services

Once running:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:3001
- **Chatbot API**: http://localhost:9000
- **Chatbot Docs**: http://localhost:9000/docs

## Useful Docker Commands

```bash
# View running containers
docker ps

# View all containers (including stopped)
docker ps -a

# View logs for a service
docker compose logs frontend
docker compose logs backend
docker compose logs chatbot

# Follow logs in real-time
docker compose logs -f

# Stop all services
docker compose down

# Stop and remove volumes
docker compose down -v

# Restart a specific service
docker compose restart backend

# Rebuild and restart
docker compose up -d --build backend
```

## Troubleshooting

### Docker IO Errors (Most Common Issue - Usually Disk Space Related)
```bash
# CRITICAL: First check available disk space - this is often the root cause!
df -h
# If disk is nearly full (< 1GB free), you MUST free up space first

# Run the disk space management script:
./manage_disk_space.sh

# Then run the IO error fix script:
./fix_docker_io_error.sh

# Or manually clean Docker system:
docker system prune -f
docker builder prune -f
docker volume prune -f

# For persistent WSL2 issues:
wsl --shutdown  # Restart WSL
# Then restart Docker Desktop
```

### Container won't start
```bash
# Check logs
docker compose logs backend

# Check container status
docker ps -a

# Try manual run to see errors
docker run -it --rm todo-backend
```

### Port already in use
```bash
# Windows: Find and kill process using port
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Or change port in docker-compose.yml:
ports:
  - "3002:3000"  # Use 3002 instead of 3000
```

### Out of disk space
```bash
# Clean up Docker
docker system prune -a
docker volume prune
```

### WSL2-Specific Issues
If running in WSL2 and experiencing build failures:

1. Move project to Linux filesystem (`/home/username/project`) instead of mounted Windows drive
2. Increase WSL disk space if needed
3. Ensure Docker Desktop is running on Windows
4. Run `./fix_docker_io_error.sh` script for common fixes

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Docker Host                          │
│                                                          │
│  ┌──────────────┐      ┌──────────────┐                │
│  │   Frontend   │─────▶│   Backend    │                │
│  │   (Next.js)  │      │  (Node/TS)   │                │
│  │   Port 3000  │      │   Port 3001  │                │
│  └──────────────┘      └──────────────┘                │
│         │                      │                         │
│         │              ┌──────────────┐                │
│         └─────────────▶│   Chatbot    │                │
│                        │  (FastAPI)   │                │
│                        │   Port 9000  │                │
│                        └──────────────┘                │
│                                                          │
│  Network: todo-network (bridge)                         │
│  Volumes: backend-data, chatbot-data                    │
└─────────────────────────────────────────────────────────┘
```

## Next Steps

1. **Fix Frontend Dependencies**:
   - Run `npm install` in `phase2/frontend`
   - Rebuild Docker image

2. **Fix Chatbot Dependencies**:
   - Pin aiohttp version in requirements.txt
   - Or increase pip timeout in Dockerfile

3. **Build All Services**:
   - Run `docker compose build`

4. **Start Application**:
   - Run `docker compose up -d`
   - Access at http://localhost:3000

5. **Configure Environment**:
   - Add API keys to `.env` file for AI features

## Files Created/Modified

### New Files:
- `docker-compose.yml` (root)
- `phase2/frontend/Dockerfile`
- `phase2/backend/Dockerfile`
- `phase2/frontend/.dockerignore`
- `phase2/backend/.dockerignore`
- `phase3/backend/.dockerignore`
- `.env.example` (root)

### Modified Files:
- `phase2/frontend/next.config.js` (enabled standalone output)
- `phase3/backend/Dockerfile` (simplified from original)

## Summary

The Docker infrastructure is ready with:
- ✅ All Dockerfiles created
- ✅ Docker Compose configuration complete
- ✅ Backend service built successfully
- ⚠️  Frontend and Chatbot need dependency resolution

The backend is ready to run. Frontend and Chatbot need minor fixes to their dependencies before building.
