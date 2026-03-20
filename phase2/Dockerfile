# Hugging Face Spaces Deployment for Hackathon Todo App
# Multi-Service Dockerfile (Backend + Frontend)

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js for frontend
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs

# Copy backend requirements and install
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy backend code
COPY backend/app /app/backend/app

# Copy frontend code
COPY frontend /app/frontend

# Install frontend dependencies
WORKDIR /app/frontend
RUN npm install
RUN npm run build

# Create startup script
WORKDIR /app
COPY <<'EOF' /app/start.sh
#!/bin/bash

# Start backend in background
cd /app/backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 4001 &

# Wait for backend to be ready
echo "Waiting for backend to start..."
sleep 5

# Start frontend
cd /app/frontend
npm run start
EOF

RUN chmod +x /app/start.sh

# Expose ports
EXPOSE 4001 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:4001/health || exit 1

# Start the application
CMD ["/app/start.sh"]
