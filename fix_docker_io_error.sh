#!/bin/bash

# Script to fix Docker IO errors in the hakathon_2 project
# Addresses the common issue: input/output error: write /var/lib/docker/buildkit/containerd-overlayfs/metadata_v2.db

echo "🔧 Fixing Docker IO Error Issues..."

# Step 1: Check available disk space
echo ""
echo "🔍 Checking available disk space..."
df -h | grep -E 'Filesystem|C:' || df -h

# Step 2: Clean Docker system
echo ""
echo "🧹 Cleaning Docker system..."
docker system prune -f
docker builder prune -f
docker volume prune -f

# Step 3: Check if Docker daemon is running properly
echo ""
echo "🔄 Checking Docker daemon status..."
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker daemon is not accessible. Please start Docker Desktop."
    exit 1
else
    echo "✅ Docker daemon is running properly"
fi

# Step 4: Try to restart Docker buildx builder (which handles BuildKit)
echo ""
echo "🔄 Restarting Docker BuildKit builder..."
docker buildx ls
docker buildx create --name mybuilder --use --bootstrap || echo "⚠️ Could not create new builder, using default"

# Step 5: Clean specific Docker directories that might have issues
echo ""
echo "🧹 Cleaning Docker cache directories (may require sudo)..."
if command -v sudo &> /dev/null; then
    # Try to clean buildkit cache if accessible
    sudo find /var/lib/docker/buildkit -name "*.db" -type f -size +1M -atime +1 -delete 2>/dev/null || echo "⚠️ Could not clean buildkit cache (normal if not running as root)"
else
    echo "⚠️ Sudo not available, skipping advanced cleanup"
fi

# Step 6: Test Docker functionality
echo ""
echo "🧪 Testing basic Docker functionality..."
if docker run --rm hello-world > /dev/null 2>&1; then
    echo "✅ Docker test successful"
else
    echo "❌ Docker test failed"
    exit 1
fi

# Step 7: Clean project-specific Docker resources
echo ""
echo "🗑️ Cleaning project-specific Docker resources..."
docker compose down -v 2>/dev/null || echo "No existing compose stack to clean"

# Remove any dangling images from this project
docker rmi $(docker images -q hakathon_2*) 2>/dev/null || echo "No project images to remove"
docker rmi $(docker images -q todo-*) 2>/dev/null || echo "No todo-* images to remove"

# Step 8: Provide next steps
echo ""
echo "✅ Docker IO error fixes applied!"
echo ""
echo "📝 Next steps:"
echo "   1. If you're using WSL2, consider increasing virtual disk space"
echo "   2. Ensure you have at least 5GB free disk space"
echo "   3. Try building again with: docker compose build"
echo "   4. If issues persist, restart Docker Desktop completely"
echo ""
echo "💡 For persistent WSL2 Docker issues, you might need to:"
echo "   - wsl --shutdown"
echo "   - Restart Docker Desktop after WSL restarts"
echo ""

exit 0