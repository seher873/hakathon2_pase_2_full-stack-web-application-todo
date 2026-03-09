# Complete Deployment Guide

## ✅ Current Status

- **Backend**: Deployed and running on Hugging Face Spaces
  - URL: https://sehrkhan873-hakathon-2.hf.space
  - Status: Healthy ✅
  
- **Frontend**: Ready for Netlify deployment
  - Configured to connect to Hugging Face backend
  - Build configuration: Complete

---

## Backend Deployment (Hugging Face Spaces)

### Current Deployment
Your backend is already deployed at: **https://sehrkhan873-hakathon-2.hf.space**

### Verify Backend Status
```bash
curl https://sehrkhan873-hakathon-2.hf.space/health
```

Expected response:
```json
{"status":"healthy","service":"ai-chatbot-backend","version":"1.0.0"}
```

### Update Backend (if needed)
Files are in: `huggingface/` directory

```bash
cd huggingface

# Initialize git (first time only)
git init
git remote add origin https://huggingface.co/spaces/sehrkhan873/hakathon-2-backend

# Push updates
git add .
git commit -m "Update backend"
git push -u origin main
```

---

## Frontend Deployment (Netlify)

### Option 1: Netlify CLI (Recommended for Quick Deployment)

```bash
# 1. Install Netlify CLI globally
npm install -g netlify-cli

# 2. Navigate to frontend directory
cd phase2/frontend

# 3. Install dependencies
npm install

# 4. Build the application
npm run build
npm run export

# 5. Login to Netlify
netlify login

# 6. Deploy to production
netlify deploy --prod --dir=out
```

### Option 2: Drag & Drop (Simplest)

```bash
# 1. Navigate to frontend directory
cd phase2/frontend

# 2. Install and build
npm install
npm run build
npm run export

# 3. Go to https://app.netlify.com/drop
# 4. Drag and drop the 'out' folder
```

### Option 3: GitHub Integration (Best for CI/CD)

1. **Push code to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Connect to Netlify:**
   - Go to https://app.netlify.com/
   - Click "Add new site" → "Import an existing project"
   - Connect to GitHub
   - Select your repository

3. **Configure build settings:**
   - **Base directory:** `phase2/frontend`
   - **Build command:** `npm install && npm run build && npm run export`
   - **Publish directory:** `out`

4. **Add environment variables:**
   - Go to Site settings → Environment variables
   - Add:
     - `NEXT_PUBLIC_API_BASE_URL` = `https://sehrkhan873-hakathon-2.hf.space`
     - `NODE_VERSION` = `20`

5. **Click "Deploy site"**

---

## Environment Variables

### Netlify Environment Variables

Set these in Netlify dashboard (Site settings → Environment variables):

| Variable | Value | Description |
|----------|-------|-------------|
| `NEXT_PUBLIC_API_BASE_URL` | `https://sehrkhan873-hakathon-2.hf.space` | Backend API URL |
| `NODE_VERSION` | `20` | Node.js version |

### Hugging Face Environment Variables

Set these in your Space settings (Settings → Variables and secrets):

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `JWT_SECRET` | JWT secret key for token generation |
| `COHERE_API_KEY` | Cohere API key (if using AI features) |
| `ALLOWED_ORIGINS` | Comma-separated list of allowed origins (e.g., `https://your-app.netlify.app`) |

---

## Post-Deployment Verification

### 1. Check Frontend Deployment
- Visit your Netlify URL (e.g., `https://your-app.netlify.app`)
- Verify the landing page loads

### 2. Test Backend Connection
- Try the AI command input on the landing page
- Check browser console for any API errors

### 3. Test Authentication
- Sign up for a new account
- Login with credentials
- Verify JWT token is stored

### 4. Test Task Management
- Create a task using natural language
- Example: "Add buy milk"
- Verify task appears in the dashboard

### 5. Test AI Integration
- Use AI commands like:
  - "Show my tasks"
  - "Complete task [task-name]"
  - "Add task finish report"

---

## Troubleshooting

### Frontend Build Fails

**Issue:** Build fails with module errors
```bash
# Solution: Clean install
rm -rf node_modules package-lock.json
npm install
npm run build
```

### API Calls Fail (CORS Errors)

**Issue:** Console shows CORS errors
```
Access to fetch at 'https://sehrkhan873-hakathon-2.hf.space' from origin 'https://your-app.netlify.app' has been blocked by CORS policy
```

**Solution:** Update backend CORS settings
1. Go to Hugging Face Space settings
2. Add your Netlify URL to `ALLOWED_ORIGINS`:
   ```
   ALLOWED_ORIGINS=https://your-app.netlify.app,http://localhost:3000
   ```
3. Redeploy the Space

### Authentication Errors (401)

**Issue:** API returns 401 Unauthorized
```json
{"detail": "Not authenticated"}
```

**Solution:** 
- Verify JWT token is being sent in requests
- Check token expiration
- Ensure `JWT_SECRET` matches between frontend and backend

### Database Connection Fails

**Issue:** Backend can't connect to database
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solution:**
- Verify `DATABASE_URL` in Hugging Face Space settings
- Check database allows external connections
- Ensure connection string format is correct

---

## Quick Commands Reference

### Backend
```bash
# Test backend health
curl https://sehrkhan873-hakathon-2.hf.space/health

# Test chat API
curl -X POST https://sehrkhan873-hakathon-2.hf.space/api/chat/message \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"message": "Hello", "user_id": "test-user"}'
```

### Frontend
```bash
# Local development
cd phase2/frontend
npm run dev

# Build for production
npm install
npm run build
npm run export

# Deploy with Netlify CLI
netlify deploy --prod --dir=out
```

---

## Deployment Checklist

- [ ] Backend deployed to Hugging Face Spaces
- [ ] Backend health check passes
- [ ] Environment variables set on Hugging Face
- [ ] Frontend builds successfully
- [ ] Environment variables set on Netlify
- [ ] Frontend deployed to Netlify
- [ ] CORS configured correctly
- [ ] Authentication flow tested
- [ ] Task CRUD operations tested
- [ ] AI commands tested
- [ ] Error handling verified

---

## Support

If you encounter issues:
1. Check the deployment logs on Netlify
2. Check Space logs on Hugging Face
3. Review browser console for errors
4. Verify all environment variables are set correctly
