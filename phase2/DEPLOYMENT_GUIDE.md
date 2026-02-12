# Phase-2 Fullstack TODO App Deployment Guide

This guide explains how to deploy the Phase-2 Fullstack TODO app to Netlify (frontend) and Hugging Face Spaces (backend).

## 🚀 Deploy to Netlify (Frontend)

### Prerequisites
- A Netlify account
- The frontend code in the `frontend/` directory

### Steps
1. Connect your GitHub repository to Netlify
2. In the Netlify build settings, configure:
   - **Build Command**: `npm run build && npm run export`
   - **Publish Directory**: `out`
3. Add environment variables:
   - `NEXT_PUBLIC_API_URL`: The URL of your deployed backend API
4. Deploy!

### Configuration Notes
- The `next.config.js` is set to `output: "export"` for static export
- The `netlify.toml` is configured to run both build and export commands
- The publish directory is set to `out` which is where Next.js exports static files

## ☁️ Deploy to Hugging Face Spaces (Backend)

### Prerequisites
- A Hugging Face account
- The backend code in the `backend/` directory

### Steps
1. Create a new Space on Hugging Face
2. Choose "Docker" as the SDK
3. Add the `space.yaml` configuration file
4. Push your code to the Space repository
5. The Space will automatically build and deploy using the Dockerfile

### Configuration Notes
- The Dockerfile is configured to be build-arg compatible for port configuration
- The space.yaml specifies the Dockerfile location and environment variables
- SQLite is used for simplicity in the Space environment
- The API will be accessible on port 7860 in the Space

## 🔗 Connecting Frontend and Backend

Once both are deployed:
1. Get the URL of your deployed backend API from Hugging Face Spaces
2. Set this URL as the `NEXT_PUBLIC_API_URL` environment variable in Netlify
3. Redeploy the frontend

## Troubleshooting

### Netlify Deployment Issues
- Make sure `npm run build && npm run export` runs successfully locally
- Verify that `next.config.js` has `output: "export"`
- Check that the publish directory is set to `out`

### Hugging Face Spaces Issues
- Ensure the Dockerfile builds successfully locally
- Check that environment variables are properly set
- Monitor the Space logs for any runtime errors

## Architecture

- **Frontend**: Next.js static site hosted on Netlify
- **Backend**: Node.js/Express API hosted on Hugging Face Spaces
- **Database**: SQLite for simplicity in the Space environment
- **Authentication**: JWT-based authentication