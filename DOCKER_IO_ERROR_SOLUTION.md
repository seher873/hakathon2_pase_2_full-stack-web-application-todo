# Docker IO Error Solution Guide

This document addresses the Docker IO error occurring in the hakathon_2 project:
```
input/output error: write /var/lib/docker/buildkit/containerd-overlayfs/metadata_v2.db
```

## Critical Root Cause: Disk Space Issue

Based on diagnostic output, the primary issue is **severely insufficient disk space**:
```
Filesystem                                Size  Used Avail Use% Mounted on
C:\                                       119G  119G  150M 100% /mnt/c
```

The disk is 100% full with only 150MB available, which is far below the minimum required for Docker operations. Docker builds require substantial temporary space for layers, cache, and intermediate files.

## Secondary Causes

Additional contributing factors to IO errors include:

1. **WSL2 Environments** - Due to filesystem translation layers between Windows and Linux
2. **Cache Corruption** - BuildKit metadata files may become corrupted when disk space is exhausted
3. **Concurrent Access Issues** - Multiple processes accessing Docker cache simultaneously

## Immediate Solutions

### 1. Run the Automated Fix Script
```bash
./fix_docker_io_error.sh
```

### 2. Manual Cleanup Commands
```bash
# Clean Docker system
docker system prune -f
docker builder prune -f
docker volume prune -f

# Remove project containers and images
docker compose down -v
docker rmi $(docker images -q hakathon_2*) 2>/dev/null || true
docker rmi $(docker images -q todo-*) 2>/dev/null || true

# Test Docker functionality
docker run --rm hello-world
```

### 3. WSL2-Specific Fixes
If using WSL2, try these additional steps:

```bash
# Shutdown WSL
wsl --shutdown

# After WSL restarts, restart Docker Desktop
# Then try the build again
```

## Long-term Prevention Strategies

### 1. Configure Docker Desktop Resources
- Open Docker Desktop Settings
- Go to Resources
- Increase Memory allocation (recommended: 6GB+)
- Increase CPU allocation (recommended: 4+ cores)
- Increase Swap allocation if needed

### 2. Configure BuildKit for Better WSL2 Compatibility
Create or update `~/.docker/config.json`:
```json
{
  "features": {
    "buildkit": true
  },
  "experimental": true,
  "builder": {
    "gc": {
      "enabled": true,
      "defaultKeepStorage": "20GB"
    }
  }
}
```

### 3. Optimize Docker Compose for IO Performance
Consider using named volumes instead of bind mounts for better performance in development:

```yaml
services:
  frontend:
    # ... existing config ...
    volumes:
      # Instead of bind mounts, use named volumes where possible
      - frontend-node-modules:/app/node_modules  # For node_modules
      # Only bind mount source code
      - ./phase2/frontend:/app:cached  # Use :cached for better WSL2 performance

volumes:
  frontend-node-modules:
```

### 4. Alternative Build Strategy
If BuildKit continues to cause issues, temporarily disable it:

```bash
# Set environment variable to disable BuildKit
export DOCKER_BUILDKIT=0
docker compose build
# Remember to unset after the build: unset DOCKER_BUILDKIT
```

## Updated Docker Compose for Better Error Handling

The following changes to `docker-compose.yml` can help prevent IO errors:

1. Add resource limits to prevent excessive disk usage
2. Configure health checks appropriately
3. Set proper restart policies

## Critical Action Required: Free Up Disk Space

**IMPORTANT**: Before attempting any Docker operations, you must address the critical disk space issue:

```bash
# Run the disk space management script first
./manage_disk_space.sh

# Verify you have at least 2-3GB free:
df -h
```

## Verification Steps

After freeing up disk space:

1. Run the disk space manager: `./manage_disk_space.sh`
2. Run the IO error fix script: `./fix_docker_io_error.sh`
3. Verify Docker is working: `docker run --rm hello-world`
4. Try a small build: `docker build -t test -f phase2/backend/Dockerfile phase2/backend`
5. If successful, build the full stack: `docker compose build`

## Recovery from Severe Cases

If the IO error persists:

1. **Complete Docker Reset**:
   - Docker Desktop → Troubleshoot → Clean / Purge data
   - Restart Docker Desktop completely

2. **WSL Distribution Optimization**:
   - Ensure you're using WSL2 (not WSL1)
   - Consider moving the project to the Linux filesystem (/home/username/) instead of Windows mounted drives

3. **Alternative Build Method**:
   ```bash
   # Build each service separately with more verbose output
   docker build -t todo-backend -f phase2/backend/Dockerfile phase2/backend
   docker build -t todo-chatbot -f phase3/backend/Dockerfile phase3/backend
   docker build -t todo-frontend -f phase2/frontend/Dockerfile phase2/frontend
   ```

## Expected Outcome

After applying these fixes:
- Docker builds should complete without IO errors
- The frontend build should succeed (previously failed due to IO errors)
- All three services (frontend, backend, chatbot) should build and run properly
- The application should be accessible at http://localhost:3000

## Monitoring

Monitor the fix by checking:
- Available disk space remains above 5GB during builds
- Docker Desktop stability during extended usage
- Build times return to normal (not excessively slow)