# Development Dockerfile for Backend Service
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy backend-specific package files from phase2/backend
COPY ./phase2/backend/package*.json ./

# Install dependencies
RUN npm install

# Copy backend application code
COPY ./phase2/backend/ ./

# Expose port for backend
EXPOSE 8000

# Start the application in development mode with hot reloading
CMD ["npm", "run", "dev"]