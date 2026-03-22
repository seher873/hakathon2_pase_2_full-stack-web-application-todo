# 🚨 Fix: Netlify Environment Variables

## Problem
Frontend is still calling `http://localhost:4001` instead of Hugging Face Space backend.

## Solution

### Option 1: Set Environment Variables on Netlify (REQUIRED)

1. **Go to Netlify Dashboard:**
   https://app.netlify.com

2. **Select your site**

3. **Go to Site settings → Environment variables**

4. **Add these variables:**

   | Key | Value |
   |-----|-------|
   | `NEXT_PUBLIC_API_BASE_URL` | `https://sehrkhan873-hakathon-2.hf.space` |
   | `NODE_VERSION` | `20` |

5. **Click "Deploy" → "Trigger deploy"**
   - Select **"Clear cache and deploy site"**

6. **Wait for rebuild** (2-3 minutes)

---

### Option 2: Update via netlify.toml (Already Done)

Your `netlify.toml` already has the correct config:

```toml
[build.environment]
  NEXT_PUBLIC_API_BASE_URL = "https://sehrkhan873-hakathon-2.hf.space"
```

But Netlify may not pick it up if:
- Site was already connected before adding netlify.toml
- Environment variables were manually set before

---

### Option 3: Redeploy with CLI

```bash
cd frontend

# Login
npx netlify-cli login

# Link to your site
npx netlify-cli link

# Set environment variables
npx netlify-cli env:set NEXT_PUBLIC_API_BASE_URL https://sehrkhan873-hakathon-2.hf.space

# Deploy with clear cache
npx netlify-cli deploy --prod --build --clearCache
```

---

## Verify Fix

After redeployment:

1. **Open your Netlify site**
2. **Open DevTools** (F12)
3. **Go to Network tab**
4. **Try to create a task**
5. **Check request URL** - should be:
   ```
   https://sehrkhan873-hakathon-2.hf.space/api/tasks
   ```
   NOT `http://localhost:4001/api/tasks`

---

## Quick Test

```javascript
// Open browser console on your Netlify site and run:
console.log(process.env.NEXT_PUBLIC_API_BASE_URL)
// Should print: https://sehrkhan873-hakathon-2.hf.space
```

---

## Common Issues

### Still showing localhost?
- **Clear browser cache** (Ctrl+Shift+Delete)
- **Hard refresh** (Ctrl+F5)
- **Try incognito mode**

### Environment variables not working?
- Make sure variable name is exactly: `NEXT_PUBLIC_API_BASE_URL`
- Must start with `NEXT_PUBLIC_` for Next.js
- Redeploy after setting variables

### Build fails?
- Check Netlify deploy logs
- Verify `NODE_VERSION = 20` is set
- Clear cache and redeploy

---

## Expected Result

After fix:
- ✅ API calls go to `https://sehrkhan873-hakathon-2.hf.space`
- ✅ No more `ERR_CONNECTION_REFUSED` errors
- ✅ Tasks create/list/delete work properly

---

**Created:** March 22, 2026
**Issue:** Frontend using localhost instead of HF Space
**Fix:** Set environment variables on Netlify
