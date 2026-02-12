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

# Copy frontend-specific package files
COPY package*.json ./

# Install dependencies as root
RUN npm install --legacy-peer-deps

# Copy frontend source files individually to avoid node_modules
COPY src ./src
COPY lib ./lib
COPY tests ./tests
COPY next.config.js ./
COPY tsconfig.json ./
COPY postcss.config.js ./
COPY tailwind.config.js ./
COPY components.json ./
COPY next-env.d.ts ./
COPY .env* ./

# Then change ownership of the app directory excluding node_modules
RUN chown -R nextjs:nodejs /app && chown -R nextjs:nodejs /app/* && chown -R nextjs:nodejs /app/.*

# Switch to non-root user
USER nextjs

# Expose port for frontend
EXPOSE 3000

# Start the application in development mode with hot reloading
# Use dumb-init to properly handle shutdown signals
ENTRYPOINT ["dumb-init", "--"]
CMD ["sh", "-c", "npm run dev -- --turbopack --hostname 0.0.0.0 --port 3000"]