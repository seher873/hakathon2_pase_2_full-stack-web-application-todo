#!/bin/bash

# Script to push Docker images to registry
# Usage: ./push-images.sh <registry-url>

set -e  # Exit on any error

if [ $# -eq 0 ]; then
    echo "Usage: $0 <registry-url>"
    echo "Example: $0 my-registry.com/user"
    exit 1
fi

REGISTRY=$1

echo "Tagging and pushing images to $REGISTRY..."

# Tag and push backend image
docker tag todo-app-backend:latest $REGISTRY/todo-app-backend:latest
docker push $REGISTRY/todo-app-backend:latest

# Tag and push chatbot image
docker tag todo-chatbot:latest $REGISTRY/todo-chatbot:latest
docker push $REGISTRY/todo-chatbot:latest

# Tag and push frontend image
docker tag todo-frontend:latest $REGISTRY/todo-frontend:latest
docker push $REGISTRY/todo-frontend:latest

echo "All images pushed successfully!"