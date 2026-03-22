# Netlify Deployment Guide - Frontend

## Backend URL
**Hugging Face Space Backend:** https://sehrkhan873-hakathon-2.hf.space

## Deployment Steps

### Option 1: Netlify CLI (Recommended)

```bash
# 1. Install Netlify CLI globally
npm install -g netlify-cli

# 2. Navigate to frontend directory
cd frontend

# 3. Install dependencies
npm install

# 4. Build the project
npm run build

# 5. Login to Netlify
netlify login

# 6. Initialize Netlify (first time only)
netlify init

# 7. Deploy to production
netlify deploy --prod
```

### Option 2: Netlify UI (Manual)

1. **Push code to GitHub** (if not already done)
   ```bash
   git add .
   git commit -m "Update backend URL for production"
   git push origin main
   ```

2. **Go to Netlify** (https://app.netlify.com)

3. **Add New Site** → Import from Git

4. **Connect to GitHub** and select your repository

5. **Configure Build Settings:**
   - **Base directory:** `frontend`
   - **Build command:** `npm install && npm run build`
   - **Publish directory:** `.next`

6. **Set Environment Variables:**
   ```
   NEXT_PUBLIC_API_BASE_URL = https://sehrkhan873-hakathon-2.hf.space
   NODE_VERSION = 20
   ```

7. **Click "Deploy Site"**

### Option 3: Drag and Drop (Quick Test)

```bash
# Build locally
cd frontend
npm install
npm run build

# Drag and drop the .next folder to Netlify Drop
# Visit: https://app.netlify.com/drop
```

## Environment Variables

| Variable | Value |
|----------|-------|
| `NEXT_PUBLIC_API_BASE_URL` | `https://sehrkhan873-hakathon-2.hf.space` |
| `NODE_VERSION` | `20` |

## Post-Deployment

1. **Test the deployment:**
   - Visit your Netlify URL (e.g., `https://your-site.netlify.app`)
   - Try creating a task
   - Check browser console for any errors

2. **If you see CORS errors:**
   - Backend already allows `*.netlify.app` origins
   - Check browser console for the exact error

3. **If API calls fail:**
   - Verify `NEXT_PUBLIC_API_BASE_URL` is set correctly
   - Check Network tab in browser DevTools

## Troubleshooting

### Build Fails
```bash
# Clear cache and rebuild
rm -rf node_modules package-lock.json
npm install
npm run build
```

### API Calls Fail
- Check if backend is running: https://sehrkhan873-hakathon-2.hf.space/health
- Verify CORS settings in backend

### Images Don't Load
- Image optimization is disabled for Netlify compatibility
- Use external image URLs or base64

## Custom Domain (Optional)

1. Go to **Domain Settings** in Netlify
2. Add your custom domain
3. Update DNS records as instructed

## Continuous Deployment

Once connected to GitHub:
- Every push to `main` will trigger automatic deployment
- Check **Deploys** tab in Netlify for build logs
