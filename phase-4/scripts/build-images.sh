#!/bin/bash

# Script to build Docker images for all services
# Usage: ./build-images.sh

set -e  # Exit on any error

echo "Building Docker images for all services..."

# Build Phase-2 backend image
echo "Building Phase-2 backend image..."
docker build -f docker/backend.Dockerfile -t todo-app-backend:latest ..

# Build Phase-3 chatbot image
echo "Building Phase-3 chatbot image..."
docker build -f docker/chatbot.Dockerfile -t todo-chatbot:latest ..

# Build frontend image
echo "Building frontend image..."
docker build -f docker/frontend.Dockerfile -t todo-frontend:latest ..

echo "All images built successfully!"
echo "Images created:"
echo "- todo-app-backend:latest"
echo "- todo-chatbot:latest" 
echo "- todo-frontend:latest"