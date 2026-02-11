#!/bin/bash

# Phase-4 Setup Script
# This script helps set up the development environment without Docker if needed

echo "Setting up Phase-4 Development Environment..."

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "Docker is not available. Setting up development environment directly..."
    
    # Check if Node.js is available
    if command -v node &> /dev/null; then
        echo "Node.js is available. Checking versions..."
        node_version=$(node --version)
        echo "Node.js version: $node_version"
        
        # Navigate to phase2 backend and install dependencies
        echo "Installing dependencies for backend..."
        cd ../phase2/backend
        npm install
        
        # Navigate to phase2 frontend and install dependencies
        echo "Installing dependencies for frontend..."
        cd ../frontend
        npm install

        echo "Development environment setup completed!"
        echo ""
        echo "To run the services manually:"
        echo "1. Backend: cd ../phase2/backend && npm run dev"
        echo "2. Frontend: cd ../phase2/frontend && npm run dev"
    else
        echo "Node.js is not available. Please install Node.js 20+ to continue."
    fi
else
    echo "Docker is available. You can use the docker-compose.dev.yml file to run the development environment."
    echo "Run: docker compose -f docker-compose.dev.yml up --build"
fi