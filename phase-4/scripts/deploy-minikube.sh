#!/bin/bash

# Script to deploy the application to Minikube
# Usage: ./deploy-minikube.sh

set -e  # Exit on any error

echo "Deploying application to Minikube..."

# Start Minikube if not running
if ! minikube status &>/dev/null; then
    echo "Starting Minikube..."
    minikube start --driver=docker
else
    echo "Minikube is already running."
fi

# Build images
./build-images.sh

# Load images into Minikube
echo "Loading images into Minikube..."
minikube image load todo-app-backend:latest
minikube image load todo-chatbot:latest
minikube image load todo-frontend:latest

# Apply Kubernetes configurations
echo "Applying Kubernetes configurations..."
kubectl apply -f ../k8s/backend-deployment.yaml
kubectl apply -f ../k8s/backend-service.yaml
kubectl apply -f ../k8s/chatbot-deployment.yaml
kubectl apply -f ../k8s/chatbot-service.yaml
kubectl apply -f ../k8s/frontend-deployment.yaml
kubectl apply -f ../k8s/frontend-service.yaml

# Wait for deployments to be ready
echo "Waiting for deployments to be ready..."
kubectl wait --for=condition=available deployment/backend-deployment --timeout=300s
kubectl wait --for=condition=available deployment/chatbot-deployment --timeout=300s
kubectl wait --for=condition=available deployment/frontend-deployment --timeout=300s

echo "Application deployed successfully!"
echo "Services are available at:"
kubectl get services