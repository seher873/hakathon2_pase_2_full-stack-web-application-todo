# Phase-4 Backend Service Deployment Guide

This document provides instructions for deploying the Phase-4 backend service to a local Minikube cluster.

## Prerequisites

- Docker (with sufficient disk space - at least 5GB free)
- Minikube
- kubectl
- Node.js (for local development/testing)

## Pre-deployment Steps

### 1. Clean Old Images
```bash
docker system prune -a
```

### 2. Ensure Sufficient Disk Space
Make sure you have at least 5GB of free disk space before proceeding with Docker operations.

### 3. Start Minikube
```bash
minikube start
```

### 4. Set Docker Environment to Use Minikube
```bash
eval $(minikube docker-env)
```

## Deployment Steps

### 1. Build Fresh Docker Image
```bash
docker build --no-cache -t phase4-backend:v1 -f Dockerfile .
```

### 2. Verify Image Was Built
```bash
docker images | grep phase4-backend
```

### 3. Deploy to Minikube
```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

### 4. Verify Deployment
```bash
kubectl get pods
kubectl get services
```

### 5. Access the Service
```bash
minikube service phase4-backend-service
```

Or get the URL directly:
```bash
minikube service phase4-backend-service --url
```

## Troubleshooting

### Pod Status Issues
If the pod is not running or in CrashLoopBackOff:
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### Service Access Issues
If you can't access the service:
```bash
kubectl get svc phase4-backend-service
```

### Clean Up
To remove the deployment and service:
```bash
kubectl delete -f service.yaml
kubectl delete -f deployment.yaml
```

## Notes

- The Dockerfile uses Node.js 20-alpine as the base image
- The application runs on port 8000 inside the container
- The service exposes the application via NodePort on port 30080
- The imagePullPolicy is set to "Never" to ensure Minikube uses the local image
- Health checks are implemented via the /health endpoint