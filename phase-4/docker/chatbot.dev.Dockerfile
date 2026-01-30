# Development Dockerfile for Chatbot Service
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY . .

# Expose port for chatbot service
EXPOSE 9000

# Start the application in development mode with hot reloading
CMD ["npm", "run", "dev"]