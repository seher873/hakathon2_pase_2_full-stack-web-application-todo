# Data Model: Docker Development Setup

## Overview
This document describes the data structures and configurations for the Docker-based development environment with volume mounts for live debugging.

## Docker Configuration Entities

### 1. Development Dockerfile Configuration

**Entity**: Dockerfile Config
- **Base Image**: node:20-alpine
- **Working Directory**: /app
- **Dependencies**: package.json and package-lock.json copied and installed
- **Source Code**: Mounted via volume mount
- **Port Exposure**: Service-specific ports (3000, 8000, 9000)
- **Development Command**: npm run dev or equivalent

**Validation Rules**:
- Base image must be node:20-alpine for consistency
- Working directory must be /app for standardization
- Dependencies must be installed before source code is copied
- Ports must match service requirements

### 2. Docker Compose Service Configuration

**Entity**: Service Config
- **Service Name**: backend, chatbot, or frontend
- **Build Context**: Path to Dockerfile
- **Container Name**: Unique identifier for each service
- **Port Mappings**: Host:Container port pairs
- **Volume Mounts**: Host directory to container directory mappings
- **Environment Variables**: NODE_ENV=development
- **Dependencies**: Service startup order dependencies

**Validation Rules**:
- Service names must be unique
- Port mappings must not conflict
- Volume mounts must include source code directories
- Dependencies must form a valid startup sequence

### 3. Volume Mount Configuration

**Entity**: Volume Mount
- **Type**: bind mount (for development)
- **Source**: Host directory path
- **Target**: Container directory path
- **Options**: Read-write access, consistent file permissions

**Validation Rules**:
- Source path must exist on host
- Target path must match working directory in Dockerfile
- Must exclude node_modules to prevent conflicts

### 4. Network Configuration

**Entity**: Docker Network
- **Network Name**: phase4-dev-network
- **Driver**: bridge (default)
- **Services**: All development services connected

**Validation Rules**:
- Network must be accessible to all services
- Services must be able to communicate via service names

## State Transitions

### Service Lifecycle States
1. **Stopped** → **Starting**: When docker-compose up is executed
2. **Starting** → **Running**: When service is ready and accepting connections
3. **Running** → **Updating**: When source code changes are detected
4. **Running** → **Stopped**: When docker-compose down is executed

### Volume Mount States
1. **Unmounted** → **Mounted**: When container starts with volume configuration
2. **Mounted** → **Syncing**: When file changes are detected and synchronized
3. **Syncing** → **Updated**: When changes are reflected in container

## Relationships

### Service Dependencies
- **Frontend** depends on **Backend** and **Chatbot**
- **Chatbot** may depend on **Backend** for API access
- **Backend** is independent but may connect to external PostgreSQL

### Network Relationships
- All services are connected to the same development network
- Services can communicate via service names (e.g., http://backend:8000)

## Configuration Examples

### Backend Service Configuration
```
backend:
  build: ...
  ports: ["8000:8000"]
  volumes: ["../../:/app", "/app/node_modules"]
  environment: ["NODE_ENV=development"]
  command: ["npm", "run", "dev"]
```

### Chatbot Service Configuration
```
chatbot:
  build: ...
  ports: ["9000:9000"]
  volumes: ["../../:/app", "/app/node_modules"]
  environment: ["NODE_ENV=development"]
  command: ["npm", "run", "dev"]
```

### Frontend Service Configuration
```
frontend:
  build: ...
  ports: ["3000:3000"]
  volumes: ["../../:/app", "/app/node_modules"]
  environment: ["NODE_ENV=development"]
  command: ["npm", "run", "dev"]
  depends_on: ["backend", "chatbot"]
```