# Production-ready Dockerfile for Phase-4 Backend Service
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache libc6-compat python3 make g++

# Copy package files
COPY ./backend/package*.json ./

# Install production dependencies only
RUN npm ci --only=production

# Copy application source code
COPY ./backend/ ./

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Change ownership of the working directory
RUN chown -R nextjs:nodejs /app
USER nextjs

# Expose port 8000 as required
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start the application
CMD ["node", "server.js"]