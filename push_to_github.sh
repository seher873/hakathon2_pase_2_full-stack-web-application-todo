#!/bin/bash

# Script to push all phases to GitHub
# This script assumes that the repository is properly initialized and connected to GitHub

set -e  # Exit on any error

echo "Preparing to push all phases to GitHub..."

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "Error: Not in a git repository. Initializing..."
    git init
fi

# Add all files to the staging area
echo "Adding all files to staging area..."
git add .

# Check for any changes
if [[ -z $(git status --porcelain) ]]; then
    echo "No changes to commit."
    exit 0
else
    echo "Changes detected. Proceeding with commit."
fi

# Commit changes
echo "Committing changes..."
git commit -m "Complete all phases - dockerization and setup

- Phase 2: Backend and frontend implementation
- Phase 3: AI Chatbot implementation
- Phase 4: Dockerization and Kubernetes deployment setup
- Added Helm charts for deployment
- Fixed Dockerfiles for React frontend
- Created deployment and cleanup scripts"

# Set the remote origin to the specified repository
REPO_URL="https://github.com/seher873/hakathon2_pase_2_full-stack-web-application-todo"

if ! git remote get-url origin &> /dev/null; then
    echo "Setting remote origin to: $REPO_URL"
    git remote add origin "$REPO_URL"
else
    echo "Updating remote origin to: $REPO_URL"
    git remote set-url origin "$REPO_URL"
fi

# Push to GitHub
echo "Pushing to GitHub..."
git branch -M main
git push -u origin main

echo "Successfully pushed all phases to GitHub!"