# Phase-4: Docker Development Setup

This setup provides a Docker-based development environment with volume mounts for live reloading during development.

## Services

- **Backend**: Runs on port 8000
- **Chatbot**: Runs on port 9000
- **Frontend**: Runs on port 3000

## Prerequisites

- Docker Engine (v20+)
- Docker Compose (v2+)

## How to Run

1. Navigate to the project root directory:
   ```bash
   cd /path/to/hakathon_2
   ```

2. Start the development environment:
   ```bash
   docker-compose -f phase-4/docker-compose.dev.yml up
   ```

3. To run in detached mode:
   ```bash
   docker-compose -f phase-4/docker-compose.dev.yml up -d
   ```

4. To stop the development environment:
   ```bash
   docker-compose -f phase-4/docker-compose.dev.yml down
   ```

## Features

- Volume mounts for live code reloading
- Isolated development environment
- Proper service dependencies
- Hot reloading enabled for all services

## Troubleshooting

- If you encounter permission issues, make sure your project directory has proper read/write permissions.
- For Node.js modules issues, try clearing the Docker volume cache:
  ```bash
  docker volume prune
  ```