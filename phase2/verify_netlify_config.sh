#!/bin/bash

# Script to verify the Next.js export configuration

echo "Verifying Next.js export configuration..."

# Check if next.config.js has the correct output setting
if grep -q 'output: "export"' /mnt/c/Users/user/Desktop/hakathon_2/phase2/frontend/next.config.js; then
    echo "✓ next.config.js has correct output setting: output: 'export'"
else
    echo "✗ next.config.js does not have correct output setting"
    exit 1
fi

# Check if netlify.toml has the correct publish directory
if grep -q 'publish = "out"' /mnt/c/Users/user/Desktop/hakathon_2/phase2/frontend/netlify.toml; then
    echo "✓ netlify.toml has correct publish directory: out"
else
    echo "✗ netlify.toml does not have correct publish directory"
    exit 1
fi

# Check if netlify.toml has the correct build command
if grep -q 'npm run build && npm run export' /mnt/c/Users/user/Desktop/hakathon_2/phase2/frontend/netlify.toml; then
    echo "✓ netlify.toml has correct build command"
else
    echo "✗ netlify.toml does not have correct build command"
    exit 1
fi

echo ""
echo "Configuration verification complete!"
echo ""
echo "Netlify Settings:"
echo "Build Command: npm run build && npm run export"
echo "Publish Directory: out"
echo ""
echo "The configuration is now correct for static export deployment to Netlify."