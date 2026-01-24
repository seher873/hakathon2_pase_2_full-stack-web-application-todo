# Feature Specification: Phase 4 - Local Kubernetes Deployment with Helm

**Feature Branch**: `003-k8s-helm-deployment`
**Created**: 2026-01-23
**Status**: Draft
**Input**: User description: "You are a senior DevOps engineer. CONTEXT: Phase-3 application is COMPLETE and WORKING: - Next.js frontend - FastAPI backend - External PostgreSQL Phase-3 code MUST NOT be modified. GOAL: Implement PHASE-4 (Local Kubernetes Deployment). STRICT RULES: 1. Work ONLY inside: phase-4/ 2. DO NOT touch Phase-1/2/3 code. 3. DO NOT modify app logic or source files. 4. NO files outside phase-4/. 5. Helm is mandatory (no raw kubectl apply). 6. Output must be runnable and error-free. PHASE-4 SCOPE: Inside phase-4/, create: - Backend Dockerfile (python:3.12-slim, non-root, health check) - Frontend Dockerfile (Next.js standalone, node:20-alpine) - Helm chart: phase-4/helm/todo-app/ - Backend + Frontend Deployments & Services - Ingress (/ → frontend, /api → backend) - ConfigMaps & Secrets (referenced, not hardcoded) - Liveness & Readiness probes - values-dev.yaml and values-prod.yaml - phase-4/README.md with exact run commands ASSUMPTIONS: - Minikube is used locally - Docker images are loaded into Minikube DELIVER: 1. phase-4 directory tree 2. Full contents of all files 3. Copy-paste ready commands only BEGIN PHASE-4 IMPLEMENTATION."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Deploy Application Locally with Helm (Priority: P1)

As a developer, I want to deploy the Phase-3 application using Kubernetes and Helm charts on my local machine so that I can test the application in a production-like environment.

**Why this priority**: This is the core functionality of the feature - enabling local Kubernetes deployment which is essential for development and testing.

**Independent Test**: Can be fully tested by running the Helm chart locally with Minikube and verifying that both frontend and backend services are accessible and communicating properly.

**Acceptance Scenarios**:

1. **Given** Minikube is running locally, **When** I execute the Helm deployment commands, **Then** both frontend and backend services are deployed and accessible
2. **Given** Application is deployed via Helm, **When** I access the frontend via browser, **Then** I can interact with the application and API calls reach the backend service

---

### User Story 2 - Configure Environment-Specific Values (Priority: P2)

As a DevOps engineer, I want to have separate values files for development and production environments so that I can customize deployments for different environments.

**Why this priority**: Essential for supporting different deployment environments with appropriate configurations.

**Independent Test**: Can be tested by deploying with different values files and verifying that the appropriate configurations are applied.

**Acceptance Scenarios**:

1. **Given** values-dev.yaml and values-prod.yaml exist, **When** I deploy with different value files, **Then** the appropriate configurations are applied to each environment

---

### User Story 3 - Access Application via Ingress (Priority: P3)

As a user, I want to access the frontend at the root path and the backend API at the /api path so that the application behaves consistently with the original setup.

**Why this priority**: Ensures the application maintains the same interface as the original Phase-3 application.

**Independent Test**: Can be tested by accessing the application through the ingress and verifying routing works correctly.

**Acceptance Scenarios**:

1. **Given** Application is deployed with ingress, **When** I navigate to the root path, **Then** I see the frontend application
2. **Given** Application is deployed with ingress, **When** I make API calls to /api path, **Then** requests are routed to the backend service

---

### Edge Cases

- What happens when Minikube is not running?
- How does the system handle insufficient resources in the local Kubernetes cluster?
- What if Docker images fail to pull during deployment?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST create Dockerfiles for both backend (using python:3.12-slim) and frontend (using node:20-alpine) applications
- **FR-002**: System MUST create a Helm chart in phase-4/helm/todo-app/ that deploys both frontend and backend services
- **FR-003**: System MUST configure ingress rules to route / to frontend and /api to backend
- **FR-004**: System MUST implement liveness and readiness probes for both frontend and backend deployments
- **FR-005**: System MUST create ConfigMaps and Secrets for application configuration
- **FR-006**: System MUST provide values-dev.yaml and values-prod.yaml for environment-specific configurations
- **FR-007**: System MUST create a README.md with exact run commands for local deployment
- **FR-008**: Dockerfiles MUST use non-root users for security purposes
- **FR-009**: Backend Dockerfile MUST include health check capabilities
- **FR-010**: Frontend Dockerfile MUST use Next.js standalone build approach

### Key Entities

- **Helm Chart**: A package that contains Kubernetes manifests and configurations for deploying the application
- **Docker Images**: Containerized versions of the frontend and backend applications
- **Ingress Controller**: Component that manages external access to services in the cluster
- **ConfigMap/Secret**: Kubernetes objects for storing configuration data and sensitive information

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can deploy the application locally using Helm in under 5 minutes
- **SC-002**: Both frontend and backend services are accessible after deployment with 99% uptime
- **SC-003**: Ingress routes requests correctly: root path serves frontend, /api path serves backend
- **SC-004**: Health checks (liveness/readiness probes) properly detect service status and restart failed containers
- **SC-005**: Documentation enables users to successfully deploy the application on their local Kubernetes environment with 95% success rate