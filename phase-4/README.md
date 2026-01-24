# Phase 4: Local Kubernetes Deployment

This document provides instructions for deploying the Todo application to a local Kubernetes cluster using Docker, Minikube, and Helm.

## Prerequisites

- Docker
- Minikube
- kubectl
- Helm
- Git

## Setup Instructions

### 1. Clone the repository (if needed)

```bash
git clone <repository-url>
cd hakathon_2
```

### 2. Start Minikube

```bash
minikube start --driver=docker
```

### 3. Build Docker Images

Build the backend image:
```bash
docker build -f phase-4/Dockerfile.backend -t todo-app-backend:latest .
```

Build the frontend image:
```bash
docker build -f phase-4/Dockerfile.frontend -t todo-app-frontend:latest .
```

### 4. Load Images into Minikube

```bash
minikube image load todo-app-backend:latest
minikube image load todo-app-frontend:latest
```

### 5. Install/Upgrade the Helm Chart

For development environment:
```bash
helm upgrade --install todo-app-dev phase-4/helm/todo-app \
  --values phase-4/helm/todo-app/values-dev.yaml \
  --namespace todo-app \
  --create-namespace
```

For production-like environment (testing purposes):
```bash
helm upgrade --install todo-app-prod phase-4/helm/todo-app \
  --values phase-4/helm/todo-app/values-prod.yaml \
  --namespace todo-app-prod \
  --create-namespace
```

### 6. Access the Application

To access the application locally, you can use port forwarding:

```bash
# Forward frontend service
kubectl port-forward -n todo-app svc/todo-app-dev-frontend 3000:3000

# Forward backend service
kubectl port-forward -n todo-app svc/todo-app-dev-backend 8000:8000
```

Alternatively, if you have an ingress controller installed:
```bash
minikube addons enable ingress
```

Then access the application at:
- Frontend: http://localhost
- Backend: http://localhost/api (for API requests)

### 7. Check Deployment Status

```bash
# Check pods
kubectl get pods -n todo-app

# Check services
kubectl get svc -n todo-app

# Check ingress
kubectl get ingress -n todo-app

# Check logs
kubectl logs -l app=backend -n todo-app
kubectl logs -l app=frontend -n todo-app
```

### 8. Uninstall the Application

```bash
helm uninstall todo-app-dev -n todo-app
kubectl delete namespace todo-app
```

## Helm Chart Configuration

The Helm chart supports the following customizable parameters:

### Backend Configuration
- `backend.image.repository`: Docker image repository for the backend
- `backend.image.tag`: Docker image tag for the backend
- `backend.replicaCount`: Number of backend replicas
- `backend.service.port`: Port for the backend service
- `backend.resources`: Resource limits and requests for the backend
- `backend.env`: Environment variables for the backend

### Frontend Configuration
- `frontend.image.repository`: Docker image repository for the frontend
- `frontend.image.tag`: Docker image tag for the frontend
- `frontend.replicaCount`: Number of frontend replicas
- `frontend.service.port`: Port for the frontend service
- `frontend.resources`: Resource limits and requests for the frontend
- `frontend.env`: Environment variables for the frontend

### Ingress Configuration
- `ingress.enabled`: Enable/disable ingress
- `ingress.hosts`: Hostnames for the ingress
- `ingress.tls`: TLS configuration for the ingress

## Environment-Specific Values

The chart includes environment-specific values files:

- `values-dev.yaml`: Optimized for local development with minimal resources
- `values-prod.yaml`: Production-ready configuration with appropriate resource allocations and autoscaling

## Security Considerations

- Both frontend and backend containers run as non-root users
- Resource limits are set to prevent resource exhaustion
- Secrets are stored separately and referenced via Kubernetes secrets
- Health checks are implemented for both services

## Deployment Automation

The project includes automated deployment scripts:

### Using the Deploy Script

The `deploy.sh` script automates the entire deployment process:

```bash
# Deploy the application (default action)
./phase-4/deploy.sh

# Deploy explicitly
./phase-4/deploy.sh deploy

# Rollback to the previous release
./phase-4/deploy.sh rollback

# Validate the current deployment
./phase-4/deploy.sh validate

# Show deployment status
./phase-4/deploy.sh status
```

### Using the Cleanup Script

The `cleanup.sh` script removes the application from the cluster:

```bash
# Remove the application deployment
./phase-4/cleanup.sh
```

## Monitoring and Logging

The application includes configurations for monitoring and logging:

- Logging levels can be adjusted via the `logging` section in values files
- Prometheus service monitors can be enabled via the `monitoring` section in values files

## Troubleshooting

### Common Issues

1. **Images not found**: Make sure to load the images into Minikube using `minikube image load`
2. **Ingress not working**: Ensure the ingress addon is enabled in Minikube: `minikube addons enable ingress`
3. **Application not responding**: Check the logs of the pods: `kubectl logs -l app=<backend|frontend> -n todo-app`
4. **Resource constraints**: Adjust resource limits in the values files according to your local machine's capabilities

### Useful Commands

```bash
# Check Helm releases
helm list -A

# Get detailed status of a release
helm status todo-app-dev -n todo-app

# Rollback to a previous release
helm rollback todo-app-dev -n todo-app

# Get all resources in the namespace
kubectl get all -n todo-app
```

### Troubleshooting Procedures

1. **Check deployment status**: Use `./phase-4/deploy.sh status` to get a comprehensive view of the deployment
2. **Validate deployment**: Run `./phase-4/deploy.sh validate` to run validation checks
3. **Rollback if needed**: Use `./phase-4/deploy.sh rollback` to revert to the previous version
4. **Review logs**: Check application logs with `kubectl logs -l app=backend -n todo-app` and `kubectl logs -l app=frontend -n todo-app`
5. **Check resources**: Verify resource allocation with `kubectl describe pods -n todo-app`
6. **Helm validation**: Run `helm lint phase-4/helm/todo-app` to validate the chart