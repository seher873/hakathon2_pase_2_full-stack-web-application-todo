#!/bin/bash

# Disk Space Management Script for hakathon_2 project
# Addresses the critical disk space issue causing Docker IO errors

echo "💾 Checking and Managing Disk Space for Docker..."

# Check current disk space
echo ""
echo "🔍 Current disk space situation:"
df -h | grep -E 'Filesystem|C:|Mounted on' || df -h

# Check if disk is critically low (less than 1GB free)
FREE_SPACE=$(df /mnt/c | awk 'NR==2 {print $4}' | sed 's/G$//')
echo ""
echo "📊 Available space: ${FREE_SPACE}G"

if (( $(echo "$FREE_SPACE < 1" | bc -l 2>/dev/null || echo "0.1") )); then
    echo "🚨 CRITICAL: Less than 1GB available. Docker operations will fail."
    echo "💡 You need to free up disk space before continuing."

    # Show Docker disk usage
    echo ""
    echo "🐳 Docker disk usage:"
    docker system df 2>/dev/null || echo "Docker not accessible"

    # Suggest cleanup actions
    echo ""
    echo "🧹 Recommended cleanup actions:"
    echo "   1. Delete unnecessary files on Windows C: drive"
    echo "   2. Empty Windows Recycle Bin"
    echo "   3. Clear Windows Temp files"
    echo "   4. Run Windows Disk Cleanup tool"
    echo "   5. Uninstall unused programs"

    # Attempt Docker cleanup anyway
    echo ""
    echo "🔧 Attempting Docker cleanup to free some space..."
    docker system prune -af 2>/dev/null || echo "Could not prune Docker system"
    docker volume prune -f 2>/dev/null || echo "Could not prune Docker volumes"
    docker builder prune -af 2>/dev/null || echo "Could not prune Docker builder cache"

    # Check space again
    FREE_SPACE_AFTER=$(df /mnt/c | awk 'NR==2 {print $4}' | sed 's/G$//')
    echo ""
    echo "📊 Available space after Docker cleanup: ${FREE_SPACE_AFTER}G"

    if (( $(echo "$FREE_SPACE_AFTER < 1" | bc -l 2>/dev/null || echo "0.1") )); then
        echo ""
        echo "❌ Still critically low on space. Cannot proceed with Docker operations."
        echo "   You must free up more disk space manually before continuing."
        exit 1
    else
        echo "✅ Docker cleanup helped. Space is now sufficient for operations."
    fi
else
    echo "✅ Disk space is adequate for Docker operations."
fi

# Additional Docker optimizations
echo ""
echo "⚙️ Performing additional Docker optimizations..."
docker system prune -f 2>/dev/null || echo "System prune skipped"
docker builder prune -f 2>/dev/null || echo "Builder prune skipped"

# Check if WSL2 specific optimizations are needed
if grep -q microsoft /proc/version; then
    echo ""
    echo "🐧 WSL2 environment detected. Additional considerations:"
    echo "   - Consider moving project to /home/username/ for better performance"
    echo "   - Large Docker builds work better on Linux filesystem than Windows mounts"
    echo "   - If issues persist, consider extending WSL disk space"
fi

echo ""
echo "✅ Disk space management complete!"
echo "   You should now have sufficient space for Docker operations."
echo ""
echo "📝 Next steps:"
echo "   1. Verify adequate space remains: df -h"
echo "   2. Try Docker operations: docker compose build"
echo "   3. Monitor space during builds: watch -n 1 'df /mnt/c'"
echo ""

exit 0