# 🚀 Hugging Face Spaces Deployment Guide

## Quick Deploy (3 Steps)

### Step 1: Get Your Hugging Face Token

1. Go to https://huggingface.co/settings/tokens
2. Click "Create new token"
3. Select "Write" permission
4. Copy the token (starts with `hf_`)

### Step 2: Run Deployment Script

```bash
cd C:\Users\user\Desktop\hakathon_2\phase2

# Option A: Using Python script (Recommended)
py deploy_hf_cli.py

# Option B: Using batch file
deploy_to_hf.bat
```

### Step 3: Enter Token When Prompted

Paste your Hugging Face token when prompted.

---

## Manual Deployment

### 1. Install huggingface_hub

```bash
py -m pip install huggingface_hub
```

### 2. Login to Hugging Face

```bash
huggingface-cli login
# Or use Python:
py -c "from huggingface_hub import login; login()"
```

### 3. Configure Git

```bash
cd C:\Users\user\Desktop\hakathon_2\phase2
git config user.name "seher873"
git config user.email "seher873@users.noreply.huggingface.co"
```

### 4. Add Hugging Face Remote

```bash
git remote add hf https://huggingface.co/spaces/sehrkhan873/HAKATHON-2.git
```

### 5. Push to Hugging Face

```bash
git add -A
git commit -m "Deploy to Hugging Face Spaces"
git push hf main
```

---

## Using Git Credential Helper

To avoid entering token every time:

```bash
# Configure git to remember credentials
git config --global credential.helper store

# Then push (enter token once)
git push hf main
```

---

## Verify Deployment

After pushing, check:

1. **Space URL**: https://huggingface.co/spaces/sehrkhan873/HAKATHON-2
2. **Build Logs**: Click "Files" → "Logs" on Space page
3. **App Status**: Should show "Running" when ready

---

## Update Deployment

```bash
# Make your changes
# Then:
git add -A
git commit -m "Update: [description]"
git push hf main
```

---

## Troubleshooting

### Authentication Failed

```bash
# Re-login
huggingface-cli login

# Or set token in environment
set HF_TOKEN=hf_xxxxx...
```

### Remote Not Found

```bash
# Remove and re-add remote
git remote remove hf
git remote add hf https://huggingface.co/spaces/sehrkhan873/HAKATHON-2.git
```

### Build Fails

1. Check build logs on Space page
2. Verify Dockerfile is correct
3. Test locally: `docker build -t test .`

---

## Space Configuration

- **SDK**: Docker
- **Port**: 4001
- **Health Check**: `/health`
- **Environment**: `DATABASE_URL=sqlite:///./app.db`

---

## Contact

- **Git User**: seher873
- **HF User**: sehrkhan873
- **Space**: sehrkhan873/HAKATHON-2
