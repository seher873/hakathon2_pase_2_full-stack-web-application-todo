# Phase-2 Backend Dockerfile
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Install dependencies
COPY package*.json ./

RUN npm ci --only=production

# Copy application code
COPY . .

# Build the application
RUN npm run build

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Change ownership of the working directory
RUN chown -R nextjs:nodejs /app
USER nextjs

# Expose port
EXPOSE 4000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:4000/health || exit 1

# Run the application
CMD ["node", "dist/server.js"]