# 🚀 Hugging Face Backend Deployment Guide

## Problem
Current HF Space pe sirf Gradio interface hai, FastAPI routes (`/api/auth/login`, `/api/tasks`, etc.) accessible nahi hain.

## Solution
HF Space ko **Gradio SDK** se **FastAPI** pe switch karna hoga.

---

## Option 1: Manual Upload via Hugging Face UI (Easiest)

### Steps:

1. **Go to your Space:**
   https://huggingface.co/spaces/sehrkhan873/HAKATHON-2

2. **Click "Files" tab**

3. **Delete existing files** (except README.md if you want)

4. **Add new files:**

   **Create `app.py`:**
   - Click "Add file" → "Create a new file"
   - Filename: `app.py`
   - Copy content from `app.py` in this project
   - Click "Commit new file"

   **Create `requirements.txt`:**
   - Click "Add file" → "Create a new file"
   - Filename: `requirements.txt`
   - Content:
     ```
     fastapi==0.109.0
     uvicorn==0.27.0
     sqlmodel==0.0.14
     python-dotenv==1.0.1
     ```
   - Click "Commit new file"

5. **Update Space SDK:**
   - Go to "Settings" tab
   - Under "Space SDK", select **Docker** (NOT Gradio)
   - Click "Save changes"

6. **Create `Dockerfile`:**
   - Click "Add file" → "Create a new file"
   - Filename: `Dockerfile`
   - Content:
     ```dockerfile
     FROM python:3.11-slim

     WORKDIR /app

     COPY requirements.txt .
     RUN pip install --no-cache-dir -r requirements.txt

     COPY app.py .

     EXPOSE 7860

     CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
     ```
   - Click "Commit new file"

7. **Wait for rebuild** (2-3 minutes)

8. **Test endpoints:**
   - Health: https://sehrkhan873-hakathon-2.hf.space/health
   - Login: https://sehrkhan873-hakathon-2.hf.space/api/auth/login
   - API Docs: https://sehrkhan873-hakathon-2.hf.space/docs

---

## Option 2: Using Git (If you have Git LFS)

```bash
# Clone the space
git clone https://huggingface.co/spaces/sehrkhan873/HAKATHON-2
cd HAKATHON-2

# Copy files
cp ../app.py .
cp ../requirements-hf.txt requirements.txt

# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 7860

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
EOF

# Commit and push
git add .
git commit -m "Deploy FastAPI backend"
git push

# Wait for rebuild
```

---

## Option 3: Using HF CLI (Python Required)

```bash
# Install HF CLI
pip install huggingface_hub

# Login
huggingface-cli login

# Upload files
huggingface-cli upload sehrkhan873/HAKATHON-2 app.py app.py
huggingface-cli upload sehrkhan873/HAKATHON-2 requirements-hf.txt requirements.txt

# Update space.yaml to use Docker
# Then wait for rebuild
```

---

## Verify Deployment

After deployment, test these endpoints:

```bash
# Health check
curl https://sehrkhan873-hakathon-2.hf.space/health

# Login
curl -X POST https://sehrkhan873-hakathon-2.hf.space/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'

# List tasks
curl https://sehrkhan873-hakathon-2.hf.space/api/tasks

# Create task
curl -X POST https://sehrkhan873-hakathon-2.hf.space/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Test task","priority":"high"}'
```

---

## Expected Response

### Login Response:
```json
{
  "status": "success",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "test@example.com",
      "created_at": "2026-03-22T...",
      "updated_at": "2026-03-22T..."
    }
  },
  "message": "Login successful",
  "timestamp": "2026-03-22T..."
}
```

---

## Troubleshooting

### "Access is denied" error
- Space is still building
- Wait 2-3 minutes and refresh

### 404 on /api/auth/login
- Make sure Dockerfile exists
- Check Space SDK is set to Docker
- Verify app.py has the /api/auth/login route

### CORS errors
- Backend allows all origins (`allow_origins=["*"]`)
- Check browser console for exact error

### Space stuck on "Building"
- Check logs in "Logs" tab
- May need to restart Space from Settings

---

## Quick Fix (Recommended)

**Go to:** https://huggingface.co/spaces/sehrkhan873/HAKATHON-2/tree/main

**Upload these 3 files:**
1. `app.py` (from this project)
2. `requirements.txt` (with fastapi, uvicorn, sqlmodel)
3. `Dockerfile` (see Option 1 above)

**Then:**
- Go to Settings → Change SDK to **Docker**
- Wait for rebuild
- Test login!

---

**Created:** March 22, 2026
**Backend:** FastAPI on Hugging Face Spaces
**Frontend:** Next.js on Netlify
