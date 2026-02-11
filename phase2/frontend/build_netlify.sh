#!/bin/bash
# Build script for deploying Phase-2 frontend to Netlify

echo "Building Phase-2 frontend for Netlify deployment..."

# Verify we're in the right directory
if [ ! -f "package.json" ] || [ ! -d "src" ]; then
    echo "Error: This script must be run from the Phase-2 frontend directory"
    exit 1
fi

echo "Installing dependencies..."
npm install

echo "Building the application..."
npm run build

echo "Exporting for static hosting..."
npm run export

# Check if the 'out' directory exists
if [ ! -d "out" ]; then
    echo "Error: 'out' directory does not exist after build and export."
    echo "This may indicate an issue with the Next.js export process."
    exit 1
fi

echo "Build complete! The 'out' directory contains the static files ready for Netlify deployment."

echo ""
echo "To deploy to Netlify:"
echo "1. Go to https://app.netlify.com/teams/seher873/projects"
echo "2. Click 'Add new site' -> 'Deploy with Netlify'"
echo "3. Connect to your GitHub repository (sehrkhan873/toDo_app_by_seher)"
echo "4. In build settings:"
echo "   - Build command: npm install && npm run build && npm run export"
echo "   - Publish directory: out"
echo "5. Add environment variables if needed"
echo "6. Click 'Deploy site'"

echo ""
echo "Alternatively, you can drag and drop the 'out' folder to Netlify's manual deploy section."