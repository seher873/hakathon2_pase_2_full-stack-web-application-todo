# Phase-2 Frontend Dockerfile
FROM node:20-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files
COPY phase2/frontend/package*.json ./
COPY phase2/frontend/next.config.js ./
COPY phase2/frontend/tsconfig.json ./

# Install dependencies
RUN npm ci

# Copy frontend source files individually to avoid node_modules
COPY phase2/frontend/src ./src
COPY phase2/frontend/lib ./lib
COPY phase2/frontend/next.config.js ./
COPY phase2/frontend/tsconfig.json ./
COPY phase2/frontend/postcss.config.js ./
COPY phase2/frontend/tailwind.config.js ./
COPY phase2/frontend/components.json ./
COPY phase2/frontend/next-env.d.ts ./
COPY phase2/frontend/.env* ./

# Build the Next.js app
RUN npm run build

# Export as standalone
RUN npm run export

# Production stage
FROM node:20-alpine

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Copy standalone output from builder stage
COPY --from=builder --chown=nextjs:nodejs /app/out /app/out

# Install serve to serve static files
RUN npm install -g serve

# Switch to non-root user
USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000 || exit 1

# Serve the app
CMD ["serve", "-s", "/app/out", "-l", "3000"]