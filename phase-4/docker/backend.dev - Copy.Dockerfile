# Development Dockerfile for Backend Service
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy backend-specific package files from phase2/backend
COPY ./phase2/backend/package*.json ./

# Install dependencies
RUN npm install

# Copy backend source files individually to avoid node_modules
COPY ./phase2/backend/src ./src
COPY ./phase2/backend/dist ./dist
COPY ./phase2/backend/tsconfig.json ./
COPY ./phase2/backend/nodemon.json ./
COPY ./phase2/backend/.env* ./


# Expose port for backend
EXPOSE 8000

# Start the application in development mode with hot reloading
CMD ["npm", "run", "dev"]