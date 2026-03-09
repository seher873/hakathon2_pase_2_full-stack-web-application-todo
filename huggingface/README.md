# Hugging Face Spaces Deployment

This directory contains the configuration for deploying the backend to Hugging Face Spaces.

## Deployment Steps

### 1. Create a new Space on Hugging Face
1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Choose:
   - **Space SDK**: Docker
   - **License**: MIT
   - **Visibility**: Public

### 2. Deploy the Backend

#### Option A: Push via Git
```bash
# Navigate to the huggingface directory
cd huggingface

# Initialize git repository (if not already initialized)
git init

# Add Hugging Face repository as remote
git remote add origin https://huggingface.co/spaces/YOUR_USERNAME/hakathon-2-backend

# Add all files and commit
git add .
git commit -m "Initial deployment"

# Push to Hugging Face
git push -u origin main
```

#### Option B: Upload Files Manually
1. Go to your Space on Hugging Face
2. Click "Files" → "Add file" → "Upload files"
3. Upload all files from this directory

### 3. Configure Environment Variables
In your Space settings, add these environment variables:
- `DATABASE_URL`: Your PostgreSQL connection string
- `JWT_SECRET`: Your JWT secret key
- `COHERE_API_KEY`: Your Cohere API key (if using AI features)
- `ALLOWED_ORIGINS`: Comma-separated list of allowed origins (e.g., `https://your-app.netlify.app`)

### 4. Verify Deployment
Once deployed, your backend will be available at:
```
https://huggingface.co/spaces/YOUR_USERNAME/hakathon-2-backend
```

The API endpoints will be at:
```
https://YOUR_USERNAME-hakathon-2-backend.hf.space/api/health
```

## Files Included

- `Dockerfile` - Docker configuration for Hugging Face Spaces
- `requirements.txt` - Python dependencies
- `app.py` - Main FastAPI application entry point
- `.dockerignore` - Files to exclude from Docker build
- `README.md` - This file

## Troubleshooting

### Build Fails
- Check the Space logs for error messages
- Ensure all dependencies are listed in requirements.txt
- Verify Dockerfile syntax

### API Not Accessible
- Check CORS settings in the backend
- Verify ALLOWED_ORIGINS environment variable
- Ensure the Space is running (not paused)

### Database Connection Issues
- Verify DATABASE_URL format
- Check network access to your database
- Ensure database allows connections from Hugging Face IPs
