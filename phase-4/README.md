# Phase-4: Containerized Deployment with Kubernetes

This directory contains all the deployment artifacts for containerizing and orchestrating the full application using Docker and Kubernetes.

## Directory Structure

```
phase-4/
├── docker/
│   ├── backend.Dockerfile        # Phase-2 backend Docker
│   ├── chatbot.Dockerfile        # Phase-3 AI chatbot Docker
│   └── frontend.Dockerfile       # Phase-3 frontend Docker
├── k8s/
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── chatbot-deployment.yaml
│   ├── chatbot-service.yaml
│   ├── frontend-deployment.yaml
│   └── frontend-service.yaml
├── env/
│   ├── backend.env.example
│   ├── chatbot.env.example
│   └── frontend.env.example
├── scripts/
│   ├── build-images.sh
│   ├── push-images.sh
│   └── deploy-minikube.sh
└── README.md
```

## Prerequisites

- Docker
- Kubernetes (or Minikube for local development)
- kubectl

## Quick Start

### 1. Build Docker Images

```bash
cd phase-4
./scripts/build-images.sh
```

### 2. Deploy to Minikube

```bash
./scripts/deploy-minikube.sh
```

### 3. Access the Application

Once deployed, you can access the services using the exposed ports:

- Frontend: `minikube service frontend-service`
- Backend: `minikube service backend-service`
- Chatbot: `minikube service chatbot-service`

## Configuration

### Environment Variables

Before deploying, copy the example environment files and fill in your values:

```bash
# For backend
cp env/backend.env.example env/backend.env

# For chatbot
cp env/chatbot.env.example env/chatbot.env

# For frontend
cp env/frontend.env.example env/frontend.env
```

### Kubernetes Secrets

Create Kubernetes secrets from your environment files:

```bash
kubectl create secret generic app-secrets \
  --from-env-file=env/backend.env \
  --from-env-file=env/chatbot.env
```

## Services

### Phase-2 Backend
- Handles user authentication and task management
- Runs on port 4000
- Connects to PostgreSQL database

### Phase-3 Chatbot
- AI-powered task management interface
- Runs on port 8000
- Integrates with Cohere API for NLP

### Frontend
- React-based user interface
- Runs on port 3000
- Communicates with both backend and chatbot services

## Scripts

- `build-images.sh`: Builds Docker images for all services
- `push-images.sh`: Tags and pushes images to a registry
- `deploy-minikube.sh`: Deploys the application to Minikube

## Production Deployment

For production deployment, update the Kubernetes configurations to:

1. Use production-grade resource limits
2. Enable horizontal pod autoscaling
3. Configure persistent volumes for databases
4. Set up SSL certificates
5. Implement proper logging and monitoring