#!/bin/bash

# Script to deploy the Todo application to Minikube using Helm

set -e  # Exit on any error

# Function to display usage
usage() {
    echo "Usage: $0 [deploy|rollback|validate|status]"
    echo "  deploy   : Deploy the application (default action)"
    echo "  rollback : Rollback to the previous release"
    echo "  validate : Validate the current deployment"
    echo "  status   : Show deployment status"
    exit 1
}

ACTION=${1:-deploy}

case $ACTION in
    deploy)
        echo "Starting deployment to Minikube..."

        # Check if minikube is running
        if ! minikube status &>/dev/null; then
            echo "Starting Minikube..."
            minikube start --driver=docker
        else
            echo "Minikube is already running."
        fi

        # Build Docker images
        echo "Building Docker images..."
        docker build -f phase-4/Dockerfile.backend -t todo-app-backend:latest . || {
            echo "Failed to build backend image"
            exit 1
        }

        docker build -f phase-4/Dockerfile.frontend -t todo-app-frontend:latest . || {
            echo "Failed to build frontend image"
            exit 1
        }

        # Load images into Minikube
        echo "Loading images into Minikube..."
        minikube image load todo-app-backend:latest || {
            echo "Failed to load backend image"
            exit 1
        }

        minikube image load todo-app-frontend:latest || {
            echo "Failed to load frontend image"
            exit 1
        }

        # Enable ingress addon
        echo "Enabling ingress addon..."
        minikube addons enable ingress || {
            echo "Failed to enable ingress addon"
            exit 1
        }

        # Install/upgrade the Helm chart
        echo "Installing/upgrading Helm chart..."
        helm upgrade --install todo-app-dev phase-4/helm/todo-app \
            --values phase-4/helm/todo-app/values-dev.yaml \
            --namespace todo-app \
            --create-namespace || {
            echo "Failed to install/upgrade Helm chart"
            exit 1
        }

        echo "Waiting for deployments to be ready..."
        kubectl wait --for=condition=available deployment/todo-app-dev-backend --namespace todo-app --timeout=300s || {
            echo "Backend deployment failed to become available"
            exit 1
        }

        kubectl wait --for=condition=available deployment/todo-app-dev-frontend --namespace todo-app --timeout=300s || {
            echo "Frontend deployment failed to become available"
            exit 1
        }

        # Run validation checks
        echo "Running validation checks..."
        ./deploy.sh validate || {
            echo "Validation failed. Rolling back..."
            ./deploy.sh rollback
            exit 1
        }

        echo ""
        echo "Deployment completed successfully!"
        echo ""
        echo "Access the application:"
        echo "- Frontend: http://localhost (if using ingress)"
        echo "- Or use port forwarding:"
        echo "  - Frontend: kubectl port-forward -n todo-app svc/todo-app-dev-frontend 3000:3000"
        echo "  - Backend: kubectl port-forward -n todo-app svc/todo-app-dev-backend 8000:8000"
        echo ""
        echo "Check status with: kubectl get pods -n todo-app"
        ;;

    rollback)
        echo "Rolling back the deployment..."
        helm rollback todo-app-dev --namespace todo-app || {
            echo "Rollback failed"
            exit 1
        }
        echo "Rollback completed successfully."
        ;;

    validate)
        echo "Validating the deployment..."

        # Check if deployments are available
        if ! kubectl get deployment todo-app-dev-backend -n todo-app &>/dev/null; then
            echo "Backend deployment not found"
            exit 1
        fi

        if ! kubectl get deployment todo-app-dev-frontend -n todo-app &>/dev/null; then
            echo "Frontend deployment not found"
            exit 1
        fi

        # Check if services are available
        if ! kubectl get service todo-app-dev-backend -n todo-app &>/dev/null; then
            echo "Backend service not found"
            exit 1
        fi

        if ! kubectl get service todo-app-dev-frontend -n todo-app &>/dev/null; then
            echo "Frontend service not found"
            exit 1
        fi

        # Check if pods are running
        BACKEND_PODS=$(kubectl get pods -n todo-app -l app=backend -o jsonpath='{.items[*].status.phase}' | tr ' ' '\n' | grep -c Running)
        FRONTEND_PODS=$(kubectl get pods -n todo-app -l app=frontend -o jsonpath='{.items[*].status.phase}' | tr ' ' '\n' | grep -c Running)

        TOTAL_BACKEND_REPLICAS=$(kubectl get deployment todo-app-dev-backend -n todo-app -o jsonpath='{.spec.replicas}')
        TOTAL_FRONTEND_REPLICAS=$(kubectl get deployment todo-app-dev-frontend -n todo-app -o jsonpath='{.spec.replicas}')

        if [ "$BACKEND_PODS" -ne "$TOTAL_BACKEND_REPLICAS" ]; then
            echo "Not all backend pods are running ($BACKEND_PODS/$TOTAL_BACKEND_REPLICAS)"
            exit 1
        fi

        if [ "$FRONTEND_PODS" -ne "$TOTAL_FRONTEND_REPLICAS" ]; then
            echo "Not all frontend pods are running ($FRONTEND_PODS/$TOTAL_FRONTEND_REPLICAS)"
            exit 1
        fi

        echo "Validation passed: All components are running correctly."
        ;;

    status)
        echo "Deployment status:"
        echo "=================="
        echo "Helm releases:"
        helm list -n todo-app
        echo ""
        echo "Pods:"
        kubectl get pods -n todo-app
        echo ""
        echo "Services:"
        kubectl get svc -n todo-app
        echo ""
        echo "Deployments:"
        kubectl get deployments -n todo-app
        ;;

    *)
        usage
        ;;
esac