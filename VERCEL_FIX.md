# 🔧 Fixing Vercel Deployment Issues

## Problem: Changes Not Showing on Vercel

If your changes aren't appearing on Vercel, follow these steps:

## ✅ Step-by-Step Fix

### 1. Verify Changes Are Committed

```bash
# Check git status
git status

# If there are uncommitted changes:
git add .
git commit -m "Update frontend with latest changes"
git push
```

### 2. Check Vercel Build Settings

In Vercel Dashboard:
1. Go to your project → **Settings** → **General**
2. Verify:
   - **Root Directory**: Leave empty (or set to project root)
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Output Directory**: `frontend/build`
   - **Install Command**: `cd frontend && npm install`

### 3. Update vercel.json

I've updated `vercel.json` to the correct configuration for frontend-only deployment.

### 4. Force Redeploy

**Option A: Via Dashboard**
1. Go to **Deployments** tab
2. Click **"..."** on latest deployment
3. Click **"Redeploy"**
4. Check **"Use existing Build Cache"** = OFF (to force fresh build)

**Option B: Via CLI**
```bash
# Install Vercel CLI if not installed
npm i -g vercel

# Login
vercel login

# Link to project (if not already linked)
vercel link

# Deploy with no cache
vercel --prod --force
```

### 5. Check Environment Variables

In Vercel Dashboard → **Settings** → **Environment Variables**:

**Required for Frontend:**
- `REACT_APP_API_URL` = `https://your-railway-app.railway.app/api`

**Important:** 
- Environment variables starting with `REACT_APP_` are embedded at build time
- If you change `REACT_APP_API_URL`, you MUST redeploy for changes to take effect

### 6. Clear Browser Cache

After deployment:
- **Hard refresh**: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
- Or open in **Incognito/Private** window

### 7. Check Build Logs

1. Go to **Deployments** tab
2. Click on the latest deployment
3. Check **Build Logs** for errors
4. Common issues:
   - Missing dependencies
   - Build errors
   - Environment variable issues

## 🔍 Troubleshooting Specific Issues

### Issue: "Build failed"

**Check:**
1. Build logs for specific error
2. All dependencies in `frontend/package.json`
3. Node version (Vercel uses Node 18 by default)

**Fix:**
```bash
# Test build locally first
cd frontend
npm install
npm run build

# If it works locally, the issue is with Vercel config
```

### Issue: "Changes not showing after redeploy"

**Possible causes:**
1. **Browser cache** - Clear cache or use incognito
2. **Build cache** - Redeploy with cache disabled
3. **Environment variables** - `REACT_APP_*` vars need rebuild
4. **Wrong branch** - Check Vercel is connected to correct branch

**Fix:**
```bash
# Force rebuild without cache
vercel --prod --force

# Or in dashboard: Redeploy → Uncheck "Use existing Build Cache"
```

### Issue: "API calls failing"

**Check:**
1. `REACT_APP_API_URL` is set correctly in Vercel
2. Backend (Railway) is running and accessible
3. CORS is configured on backend
4. API URL format: `https://your-backend.railway.app/api` (with `/api`)

**Fix:**
```javascript
// In frontend/src/services/api.js
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
```

### Issue: "404 errors on routes"

**Check:**
1. `vercel.json` has correct routing
2. React Router is configured for client-side routing
3. Output directory is correct

**Fix:**
- The updated `vercel.json` should handle this correctly

## 📋 Quick Checklist

- [ ] Changes committed and pushed to git
- [ ] Vercel connected to correct repository and branch
- [ ] Build command: `cd frontend && npm install && npm run build`
- [ ] Output directory: `frontend/build`
- [ ] `REACT_APP_API_URL` set in Vercel environment variables
- [ ] Redeployed with cache disabled
- [ ] Browser cache cleared
- [ ] Build logs show successful build
- [ ] No errors in deployment logs

## 🚀 Recommended: Use Vercel Dashboard Settings

Instead of relying on `vercel.json`, configure in dashboard:

1. **Settings** → **General**
   - **Framework Preset**: Create React App
   - **Root Directory**: (leave empty)
   - **Build Command**: `cd frontend && npm run build`
   - **Output Directory**: `frontend/build`
   - **Install Command**: `cd frontend && npm install`

2. **Settings** → **Environment Variables**
   - Add: `REACT_APP_API_URL` = `https://your-railway-app.railway.app/api`

3. **Deployments** → **Redeploy** (with cache disabled)

## 🎯 Alternative: Deploy Frontend to Railway Instead

If Vercel continues to cause issues, deploy frontend to Railway:

1. Create new service in Railway
2. Set build command: `cd frontend && npm install && npm run build`
3. Set start command: `npx serve -s frontend/build -l $PORT`
4. Deploy

This keeps everything in one place and is often easier!

## 📞 Still Having Issues?

1. **Check Vercel build logs** - Look for specific error messages
2. **Test build locally** - `cd frontend && npm run build`
3. **Verify git push** - Make sure changes are in the repository
4. **Check branch** - Vercel might be watching wrong branch
5. **Contact Vercel support** - If build logs show platform issues

