# Development Dockerfile for Frontend Service
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy frontend-specific package files from phase2/frontend
COPY ./phase2/frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy frontend application code
COPY ./phase2/frontend/ ./

# Expose port for frontend
EXPOSE 3000

# Start the application in development mode with hot reloading
CMD ["npm", "run", "dev"]