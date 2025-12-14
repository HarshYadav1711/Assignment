# 🔧 Fixing "Not Found" Error on Railway

## Problem
When you visit your Railway app URL, you see "Not Found" error.

## Solution

I've added a root route (`/`) to your Flask app. Now when you visit the Railway URL, you'll see API information instead of an error.

## What Changed

Added a root endpoint in `backend/app.py`:
```python
@app.route('/', methods=['GET'])
def root():
    """Root endpoint - API information"""
    return jsonify({
        'message': 'AI Study Tool API',
        'status': 'running',
        ...
    })
```

## Next Steps

### Option 1: Deploy Frontend Separately (Recommended)

1. **Deploy Frontend to Vercel**:
   - Build frontend: `cd frontend && npm run build`
   - Deploy to Vercel (see `DEPLOY_VERCEL.md`)
   - Set environment variable: `REACT_APP_API_URL=https://your-railway-app.railway.app/api`

2. **Backend stays on Railway**:
   - Your Railway URL is just for API calls
   - Frontend makes requests to `https://your-railway-app.railway.app/api/...`

### Option 2: Serve Frontend from Flask (Alternative)

If you want to serve the frontend from the same Railway deployment:

1. **Build the frontend**:
   ```bash
   cd frontend
   npm run build
   ```

2. **Update Flask app** to serve static files:
   ```python
   @app.route('/', defaults={'path': ''})
   @app.route('/<path:path>')
   def serve_frontend(path):
       if path != "" and os.path.exists(os.path.join('frontend/build', path)):
           return send_from_directory('frontend/build', path)
       else:
           return send_from_directory('frontend/build', 'index.html')
   ```

3. **Update Procfile**:
   ```
   web: gunicorn --chdir backend app:app --bind 0.0.0.0:$PORT
   ```

4. **Copy build folder** to backend or project root before deploying

## Verify It's Working

1. Visit your Railway URL: `https://your-app.railway.app`
   - Should show API information JSON

2. Test health endpoint: `https://your-app.railway.app/api/health`
   - Should return: `{"status": "healthy", ...}`

3. Test chat endpoint: `https://your-app.railway.app/api/chat`
   - Should return error (needs POST with data) or method not allowed

## Current Status

✅ Root route added - no more "Not Found" error
✅ API endpoints working
✅ Ready for frontend to connect

## Deploy the Fix

1. **Commit and push**:
   ```bash
   git add backend/app.py
   git commit -m "Add root route to fix Railway Not Found error"
   git push
   ```

2. **Railway will auto-deploy** - check the deployment logs

3. **Visit your Railway URL** - should now show API info instead of "Not Found"

