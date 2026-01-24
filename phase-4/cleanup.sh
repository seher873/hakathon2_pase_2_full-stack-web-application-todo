#!/bin/bash

# Script to clean up the Todo application deployment from Minikube

set -e  # Exit on any error

echo "Starting cleanup of Todo application deployment..."

# Uninstall the Helm release
echo "Uninstalling Helm release..."
helm uninstall todo-app-dev -n todo-app || {
    echo "Warning: Failed to uninstall Helm release (may not exist)"
}

# Delete the namespace
echo "Deleting namespace..."
kubectl delete namespace todo-app --ignore-not-found=true

# Optionally remove Docker images from Minikube (uncomment if needed)
# echo "Removing Docker images from Minikube..."
# minikube image rm todo-app-backend:latest || true
# minikube image rm todo-app-frontend:latest || true

echo ""
echo "Cleanup completed successfully!"
echo ""
echo "Remaining resources can be checked with: kubectl get all -A"