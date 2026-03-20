# Hugging Face Spaces Deployment Guide

## Quick Deploy

### Option 1: One-Click Deploy (Recommended)

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Choose:
   - **Space Name**: `hackathon-todo-app`
   - **License**: MIT
   - **SDK**: Docker
4. Click "Create Space"
5. Push code to the space:

```bash
# Add Hugging Face as remote
cd C:\Users\user\Desktop\hakathon_2\phase2
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/hackathon-todo-app

# Push to Hugging Face
git push hf main
```

### Option 2: Manual Deploy

#### Step 1: Create Space on Hugging Face

1. Visit https://huggingface.co/new-space
2. Enter space details:
   - **Space name**: `hackathon-todo-app`
   - **License**: MIT
   - **SDK**: Docker
3. Click "Create Space"

#### Step 2: Configure Space Settings

In your Space settings:
- Set **Port**: 4001
- Set **Health Check Path**: `/health`
- Add environment variables if needed

#### Step 3: Push Code

```bash
# Navigate to project
cd C:\Users\user\Desktop\hakathon_2\phase2

# Initialize git if not already done
git init
git add .
git commit -m "Initial commit for HF Spaces"

# Add Hugging Face remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/hackathon-todo-app

# Push to Hugging Face
git push -u hf main
```

#### Step 4: Wait for Build

- Hugging Face will automatically build your Docker container
- Build time: ~5-10 minutes
- Status shown in Space page

#### Step 5: Access Your App

Once deployed, access at:
```
https://YOUR_USERNAME-hackathon-todo-app.hf.space
```

## Files Included

```
phase2/
├── backend/
│   ├── Dockerfile           # Backend Docker config
│   ├── .dockerignore        # Docker ignore rules
│   ├── requirements.txt     # Python dependencies
│   └── app/
│       ├── main.py          # FastAPI app
│       ├── models.py        # Database models
│       ├── schemas.py       # Pydantic schemas
│       ├── crud.py          # Database operations
│       ├── routes.py        # Task routes
│       ├── chatbot.py       # AI chatbot
│       └── auth.py          # Authentication
├── README.md                # Documentation
├── space.yaml               # HF Spaces config
└── Dockerfile               # Full app Docker config
```

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | Database connection | `sqlite:///./app.db` | No |
| `PORT` | Server port | `4001` | No |
| `HF_TOKEN` | Hugging Face token (optional) | - | No |

## Testing After Deploy

### Health Check
```bash
curl https://YOUR_USERNAME-hackathon-todo-app.hf.space/health
```

### Create Task
```bash
curl -X POST https://YOUR_USERNAME-hackathon-todo-app.hf.space/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Test task","priority":"high"}'
```

### AI Chatbot
```bash
curl -X POST https://YOUR_USERNAME-hackathon-todo-app.hf.space/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Add buy milk"}'
```

## Troubleshooting

### Build Fails

1. Check build logs in Space page
2. Common issues:
   - Missing dependencies in `requirements.txt`
   - Docker build errors
   - Port configuration

### App Not Starting

1. Check container logs
2. Verify health check endpoint: `/health`
3. Ensure port 4001 is exposed

### Database Issues

- SQLite is used by default (file-based)
- For production, use PostgreSQL:
  ```
  DATABASE_URL=postgresql://user:pass@host:5432/dbname
  ```

## Updating Deployment

```bash
# Make changes
git add .
git commit -m "Update: [description]"

# Push to Hugging Face
git push hf main

# Space will auto-rebuild
```

## Resources

- [Hugging Face Spaces Docs](https://huggingface.co/docs/hub/spaces)
- [Docker on Spaces](https://huggingface.co/docs/hub/spaces-sdks-docker)
- [Environment Variables](https://huggingface.co/docs/hub/spaces-overview#managing-secrets)

## Support

For issues:
1. Check Space logs
2. Review Docker build output
3. Test locally first: `docker build -t todo-app . && docker run -p 4001:4001 todo-app`
