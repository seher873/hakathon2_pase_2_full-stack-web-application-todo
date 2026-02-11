# Development Dockerfile for Frontend Service
FROM node:20-alpine

# Install build dependencies for native modules
RUN apk add --no-cache libc6-compat python3 make g++

# Set working directory
WORKDIR /app

# Install dumb-init to properly handle signals in Docker
RUN apk add --no-cache dumb-init

# Create a non-root user to avoid potential permission issues
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Copy frontend-specific package files from phase2/frontend
COPY ./phase2/frontend/package*.json ./

# Install dependencies as root
RUN npm install --legacy-peer-deps

# Copy frontend source files individually to avoid node_modules
COPY ./phase2/frontend/src ./src
COPY ./phase2/frontend/lib ./lib
COPY ./phase2/frontend/tests ./tests
COPY ./phase2/frontend/next.config.js ./
COPY ./phase2/frontend/tsconfig.json ./
COPY ./phase2/frontend/postcss.config.js ./
COPY ./phase2/frontend/tailwind.config.js ./
COPY ./phase2/frontend/components.json ./
COPY ./phase2/frontend/next-env.d.ts ./
COPY ./phase2/frontend/.env* ./

# Change ownership of the working directory
RUN chown -R nextjs:nodejs /app
USER nextjs

# Expose port for frontend
EXPOSE 3000

# Start the application in development mode with hot reloading
# Use dumb-init to properly handle shutdown signals
ENTRYPOINT ["dumb-init", "--"]
CMD ["sh", "-c", "npm run dev -- --hostname 0.0.0.0 --port 3000"]