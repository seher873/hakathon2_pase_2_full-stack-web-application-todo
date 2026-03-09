#!/bin/bash

# Netlify Deployment Script for AI Todo Frontend
# This script builds and deploys the frontend to Netlify

set -e

echo "🚀 Starting Netlify Deployment..."

# Navigate to frontend directory
FRONTEND_DIR="phase2/frontend"

if [ ! -d "$FRONTEND_DIR" ]; then
    echo "❌ Frontend directory not found: $FRONTEND_DIR"
    exit 1
fi

cd "$FRONTEND_DIR"

echo "📦 Installing dependencies..."
npm install

echo "🔨 Building application..."
npm run build
npm run export

echo "✅ Build complete!"
echo ""
echo "📁 Static files are in: out/"
echo ""
echo "To deploy to Netlify, choose one of these options:"
echo ""
echo "Option 1: Netlify CLI (Recommended)"
echo "  npm install -g netlify-cli"
echo "  netlify login"
echo "  netlify deploy --prod --dir=out"
echo ""
echo "Option 2: Manual upload"
echo "  Upload the 'out' folder to https://app.netlify.com/drop"
echo ""
echo "Option 3: GitHub Integration"
echo "  Push to GitHub and connect to Netlify"
echo "  Build command: npm install && npm run build && npm run export"
echo "  Publish directory: out"
echo ""
echo "Environment Variables to set on Netlify:"
echo "  NEXT_PUBLIC_API_BASE_URL=https://sehrkhan873-hakathon-2.hf.space"
echo "  NODE_VERSION=20"
echo ""
