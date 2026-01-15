#!/bin/bash

# Netlify build script for the multi-phase project

# Set the working directory to the frontend
cd phase2/frontend

# Install dependencies
npm install

# Build the project
npm run build

# The output will be in the out directory which Netlify will publish
echo "Build completed successfully"