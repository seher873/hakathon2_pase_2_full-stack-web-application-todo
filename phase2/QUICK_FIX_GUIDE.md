# 🚀 Hugging Face Space Update - Step by Step

## Backend ko fix karne ke liye yeh steps follow karein:

---

## Step 1: Open Hugging Face Space Files

**URL:** https://huggingface.co/spaces/sehrkhan873/HAKATHON-2/tree/main

---

## Step 2: Delete Old app.py

1. **Click on `app.py`** file
2. **Click "Edit"** button (top right)
3. **Delete ALL content** (Ctrl+A, Delete)
4. **DON'T save yet**

---

## Step 3: Copy New Code

1. Open file: **`app-hf.py`** (from this folder)
2. **Copy ALL content** (Ctrl+A, Ctrl+C)

---

## Step 4: Paste & Save

1. Go back to HF Space `app.py` edit tab
2. **Paste the code** (Ctrl+V)
3. **Scroll down** to bottom
4. **Click "Commit changes to main"**

---

## Step 5: Update requirements.txt

1. **Click on `requirements.txt`**
2. **Click "Edit"**
3. **Replace content** with:
   ```
   fastapi==0.109.0
   uvicorn==0.27.0
   sqlmodel==0.0.14
   ```
4. **Click "Commit changes to main"**

---

## Step 6: Wait for Rebuild

1. Go to: https://huggingface.co/spaces/sehrkhan873/HAKATHON-2
2. **Click "Logs" tab**
3. **Wait 2-3 minutes** for rebuild
4. Status should change from "Building" → "Running"

---

## Step 7: Test Login

**Test URL:** https://sehrkhan873-hakathon-2.hf.space/api/auth/login

**Using Browser:**
```
Open: https://sehrkhan873-hakathon-2.hf.space/api/auth/login
Method: POST
Headers: Content-Type: application/json
Body: {"email":"test@test.com","password":"test"}
```

**Expected Response:**
```json
{
  "status": "success",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "test@example.com",
      ...
    }
  },
  "message": "Login successful",
  ...
}
```

---

## ✅ Success Checklist

- [ ] app.py updated with new code
- [ ] requirements.txt updated
- [ ] Space rebuilt (status = "Running")
- [ ] /health endpoint works
- [ ] /api/auth/login returns 200 (not 404)
- [ ] Frontend (Netlify) pe login kaam karta hai

---

## 🆘 Agar Problem Ho

### "Building" stuck hai
- Refresh the page
- Check "Logs" tab for errors

### Still 404 on /api/auth/login
- Make sure app.py was saved correctly
- Check file size should be ~10KB (not 224 bytes)

### CORS error on frontend
- Backend already allows all origins (*)
- Clear browser cache and retry

---

## 📞 Quick Links

| What | URL |
|------|-----|
| Space Home | https://huggingface.co/spaces/sehrkhan873/HAKATHON-2 |
| Files | https://huggingface.co/spaces/sehrkhan873/HAKATHON-2/tree/main |
| Health Check | https://sehrkhan873-hakathon-2.hf.space/health |
| API Docs | https://sehrkhan873-hakathon-2.hf.space/docs |
| Login Test | https://sehrkhan873-hakathon-2.hf.space/api/auth/login |

---

**Total Time:** 2-3 minutes
**Difficulty:** Easy (Copy → Paste → Commit)
