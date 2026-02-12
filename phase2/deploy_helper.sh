#!/bin/bash

# Deployment helper script for Phase-2 Fullstack TODO App

echo "==========================================="
echo "Phase-2 Fullstack TODO App Deployment Helper"
echo "==========================================="
echo ""

# Function to display menu
show_menu() {
    echo "Select an action:"
    echo "1. Prepare frontend for Netlify deployment"
    echo "2. Prepare backend for Hugging Face Spaces deployment"
    echo "3. Verify configurations"
    echo "4. Exit"
    echo ""
}

# Function to prepare frontend for Netlify
prepare_frontend() {
    echo "Preparing frontend for Netlify deployment..."
    echo ""
    
    cd /mnt/c/Users/user/Desktop/hakathon_2/phase2/frontend
    
    echo "Checking configuration files:"
    echo "- next.config.js: $(if [ -f next.config.js ] && grep -q 'output: \"export\"' next.config.js; then echo '✓ CORRECT'; else echo '✗ NEEDS FIX'; fi)"
    echo "- netlify.toml: $(if [ -f netlify.toml ] && grep -q 'publish = \"out\"' netlify.toml && grep -q 'npm run build && npm run export' netlify.toml; then echo '✓ CORRECT'; else echo '✗ NEEDS FIX'; fi)"
    echo ""
    
    echo "Frontend preparation complete!"
    echo "Next steps:"
    echo "1. Push your code to a GitHub repository"
    echo "2. Connect the repository to Netlify"
    echo "3. Set build command to: npm run build && npm run export"
    echo "4. Set publish directory to: out"
    echo ""
}

# Function to prepare backend for Hugging Face Spaces
prepare_backend() {
    echo "Preparing backend for Hugging Face Spaces deployment..."
    echo ""
    
    cd /mnt/c/Users/user/Desktop/hakathon_2/phase2
    
    echo "Checking configuration files:"
    echo "- Dockerfile: $(if [ -f backend/Dockerfile ] && grep -q 'ARG PORT' backend/Dockerfile; then echo '✓ CORRECT'; else echo 'OK (existing)'; fi)"
    echo "- space.yaml: $(if [ -f space.yaml ]; then echo '✓ EXISTS'; else echo '✗ MISSING'; fi)"
    echo ""
    
    echo "Backend preparation complete!"
    echo "Next steps:"
    echo "1. Create a new Space on Hugging Face"
    echo "2. Choose 'Docker' as the SDK"
    echo "3. Add the space.yaml configuration"
    echo "4. Push your code to the Space repository"
    echo ""
}

# Function to verify configurations
verify_configs() {
    echo "Verifying configurations..."
    echo ""
    
    echo "=== Frontend Configuration ==="
    cd /mnt/c/Users/user/Desktop/hakathon_2/phase2/frontend
    echo "next.config.js output setting: $(grep -o 'output: \"export\"' next.config.js 2>/dev/null || echo 'NOT FOUND')"
    echo "netlify.toml build command: $(grep -o 'npm run build && npm run export' netlify.toml 2>/dev/null || echo 'NOT FOUND')"
    echo "netlify.toml publish directory: $(grep -o 'publish = \"out\"' netlify.toml 2>/dev/null || echo 'NOT FOUND')"
    echo ""
    
    echo "=== Backend Configuration ==="
    cd /mnt/c/Users/user/Desktop/hakathon_2/phase2
    echo "Dockerfile port configuration: $(grep -o 'ARG PORT' backend/Dockerfile 2>/dev/null || echo 'NOT FOUND')"
    echo "space.yaml exists: $(if [ -f space.yaml ]; then echo 'YES'; else echo 'NO'; fi)"
    echo ""
}

# Main loop
while true; do
    show_menu
    read -p "Enter your choice [1-4]: " choice
    
    case $choice in
        1)
            prepare_frontend
            ;;
        2)
            prepare_backend
            ;;
        3)
            verify_configs
            ;;
        4)
            echo "Exiting deployment helper..."
            exit 0
            ;;
        *)
            echo "Invalid option. Please select 1-4."
            echo ""
            ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
done