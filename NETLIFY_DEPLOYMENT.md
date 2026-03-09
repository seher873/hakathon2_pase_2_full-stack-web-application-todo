# Netlify Deployment Guide

## ✅ Configuration Updated

The frontend has been configured to connect to the backend at:
**https://sehrkhan873-hakathon-2.hf.space**

## Files Modified

1. **phase2/frontend/netlify.toml** - Updated with backend URL and build settings
2. **phase2/frontend/next.config.js** - Configured for static export
3. **phase2/frontend/.env.production** - Production environment variables
4. **phase2/frontend/src/utils/config.ts** - Updated to use NEXT_PUBLIC_API_BASE_URL

## Deployment Options

### Option 1: Deploy via Netlify CLI (Recommended)

```bash
# Install Netlify CLI globally
npm install -g netlify-cli

# Navigate to frontend directory
cd phase2/frontend

# Build the application
npm install
npm run build
npm run export

# Login to Netlify
netlify login

# Deploy
netlify deploy --prod --dir=out
```

### Option 2: Deploy via GitHub Integration

1. Push code to GitHub repository
2. Go to https://app.netlify.com/
3. Click "Add new site" → "Import an existing project"
4. Connect to GitHub and select your repository
5. Configure build settings:
   - **Base directory:** `phase2/frontend`
   - **Build command:** `npm install && npm run build && npm run export`
   - **Publish directory:** `out`
6. Add environment variable:
   - `NEXT_PUBLIC_API_BASE_URL=https://sehrkhan873-hakathon-2.hf.space`
7. Click "Deploy site"

### Option 3: Manual Drag & Drop

```bash
# Build the application
cd phase2/frontend
npm install
npm run build
npm run export

# The 'out' directory contains static files
# Drag and drop 'out' folder to https://app.netlify.com/drop
```

## Environment Variables

Set these in Netlify dashboard (Site settings → Environment variables):

| Variable | Value |
|----------|-------|
| `NEXT_PUBLIC_API_BASE_URL` | `https://sehrkhan873-hakathon-2.hf.space` |
| `NODE_VERSION` | `20` |

## Verify Deployment

After deployment, test the following:

1. **Health Check:** Visit your Netlify URL
2. **Backend Connection:** Test API calls to the backend
3. **Authentication:** Login/signup flow
4. **Task Management:** Create, update, delete tasks

## Troubleshooting

### Build Fails
- Check Node.js version (should be 20)
- Clear `.next` and `node_modules` folders
- Run `npm install` again

### API Calls Fail
- Verify `NEXT_PUBLIC_API_BASE_URL` is set correctly
- Check CORS settings on backend
- Ensure backend is running and accessible

### Static Export Issues
- Ensure `output: 'export'` is in next.config.js
- Check that `images.unoptimized = true` is set

## Quick Commands

```bash
# Local development
cd phase2/frontend
npm run dev

# Build for production
npm run build
npm run export

# Deploy to Netlify
netlify deploy --prod --dir=out
```
