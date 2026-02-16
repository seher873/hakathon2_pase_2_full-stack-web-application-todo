FROM node:20-alpine

WORKDIR /app

# Copy package files from Phase2 backend
COPY ./phase2/backend/package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY ./phase2/backend/src ./src
COPY ./phase2/backend/tsconfig.json ./

# Build the application
RUN npm run build

# Expose port
EXPOSE 4001

# Run the application
CMD ["node", "dist/server.js"]