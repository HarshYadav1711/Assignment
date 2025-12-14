# 🚂 Deploying to Railway - Recommended Method

Railway is **perfect** for this Flask + React project. No code changes needed!

## ✅ Why Railway?

- ✅ Full Flask app support (no serverless conversion)
- ✅ Built-in PostgreSQL database
- ✅ Persistent file storage
- ✅ Easy environment variable management
- ✅ Free tier available ($5 credit/month)
- ✅ Simple deployment

## 🚀 Step-by-Step Deployment

### Step 1: Prepare Your Project

1. **Ensure `.env` is in `.gitignore`** (already done)
2. **Create `Procfile`** for Railway:
   ```
   web: cd backend && python app.py
   ```
3. **Create `railway.json`** (optional, for configuration)

### Step 2: Set Up Railway Account

1. Go to https://railway.app
2. Sign up with GitHub
3. Create new project

### Step 3: Deploy Backend

#### Option A: Using Railway Dashboard (Easiest)

1. **Click "New Project"** → "Deploy from GitHub repo"
2. **Select your repository**
3. **Railway will auto-detect** Python project
4. **Add PostgreSQL**:
   - Click "+ New" → "Database" → "Add PostgreSQL"
   - Railway creates database automatically

5. **Set Environment Variables**:
   - Click on your service → "Variables"
   - Add all variables from `.env.example`:
     ```
     OPENAI_API_KEY=your_key
     SECRET_KEY=your_secret_key
     FLASK_DEBUG=False
     DATABASE_URL=${{Postgres.DATABASE_URL}}
     LLM_PROVIDER=openai
     OPENAI_MODEL=gpt-4-turbo-preview
     OPENAI_EMBEDDING_MODEL=text-embedding-3-small
     # ... etc
     ```

6. **Configure Build** (usually auto-detected):
   - Settings → Build Command: `pip install -r requirements.txt` (auto-detected)
   - Settings → Start Command: `gunicorn --chdir backend app:app --bind 0.0.0.0:$PORT`
   - **OR** Railway will auto-detect Flask and use gunicorn automatically

7. **Deploy**: Railway auto-deploys on git push!

#### Option B: Using Railway CLI

```bash
# 1. Install Railway CLI
npm i -g @railway/cli

# 2. Login
railway login

# 3. Initialize project
railway init

# 4. Add PostgreSQL database
railway add postgresql

# 5. Link to existing project (if needed)
railway link

# 6. Set environment variables
railway variables set OPENAI_API_KEY=your_key
railway variables set SECRET_KEY=your_secret_key
railway variables set FLASK_DEBUG=False
# ... add all variables

# 7. Deploy
railway up
```

### Step 4: Update Database Configuration

Railway provides `DATABASE_URL` automatically. Update your `.env` or config:

```python
# Railway automatically provides DATABASE_URL
# Format: postgresql://user:password@host:port/dbname
# Your config.py will pick it up automatically
```

### Step 5: Deploy Frontend

#### Option A: Deploy to Vercel (Recommended for Frontend)

1. **Build frontend**:
   ```bash
   cd frontend
   npm run build
   ```

2. **Deploy to Vercel**:
   ```bash
   npm i -g vercel
   vercel
   ```

3. **Update API URL**:
   - In `frontend/src/services/api.js`
   - Change `API_BASE_URL` to your Railway backend URL:
     ```javascript
     const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://your-app.railway.app/api';
     ```

#### Option B: Deploy Frontend to Railway Too

1. **Create separate service** in Railway
2. **Set build command**: `cd frontend && npm install && npm run build`
3. **Set start command**: `cd frontend && npx serve -s build -l 3000`
4. **Add static file serving** or use Railway's static site feature

### Step 6: Configure CORS

Update `backend/app.py` to allow your frontend domain:

```python
CORS(app, origins=[
    "http://localhost:3000",  # Local dev
    "https://your-frontend.vercel.app",  # Production
])
```

### Step 7: Set Up File Storage

Railway has persistent storage, but for production, consider:

- **Cloudinary** for media files (recommended)
- **AWS S3** for large files
- **Railway volumes** for temporary files

### Step 8: Update RAG Engine

For production, consider:
- **Pinecone** for vector search (scalable)
- Or keep FAISS but initialize on startup (Railway supports this)

## 📝 Railway Configuration Files

### `Procfile` (for Railway)

```
web: gunicorn --chdir backend app:app --bind 0.0.0.0:$PORT
```

**Note**: Railway will auto-detect Flask and use gunicorn if Procfile is missing, but it's better to specify it explicitly.

### `railway.json` (optional)

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python run_backend.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

## 🔧 Environment Variables for Railway

Set these in Railway dashboard:

```
# Flask
SECRET_KEY=generate-a-secure-key
FLASK_DEBUG=False

# Database (Railway provides this automatically)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# OpenAI
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# LLM
LLM_PROVIDER=openai

# RAG Settings
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5
SIMILARITY_THRESHOLD=0.7

# Audio/TTS
TTS_PROVIDER=openai
TEACHER_VOICE=alloy
STUDENT_VOICE=nova

# Media (optional - use Cloudinary for production)
VIDEO_OUTPUT_DIR=/tmp/videos
AUDIO_OUTPUT_DIR=/tmp/audio
```

## 🎯 Post-Deployment Checklist

- [ ] Backend is accessible at Railway URL
- [ ] Database connection works
- [ ] Frontend connects to backend API
- [ ] CORS is configured correctly
- [ ] Environment variables are set
- [ ] RAG engine initializes successfully
- [ ] File uploads/storage works
- [ ] Health check endpoint works: `/api/health`

## 🔗 Useful Railway Commands

```bash
# View logs
railway logs

# Open shell
railway shell

# View variables
railway variables

# Open database
railway connect postgresql

# Deploy
railway up
```

## 💡 Tips

1. **Use Railway's PostgreSQL**: It's free and automatically managed
2. **Monitor usage**: Railway shows resource usage in dashboard
3. **Set up alerts**: Configure notifications for errors
4. **Use Railway domains**: Free `.railway.app` domain included
5. **Custom domain**: Add your own domain in settings

## 🆘 Troubleshooting

### Database Connection Issues
- Check `DATABASE_URL` is set correctly
- Verify PostgreSQL service is running
- Check connection string format

### Import Errors
- Ensure all dependencies in `requirements.txt`
- Check Python version (Railway uses 3.11 by default)

### RAG Initialization Fails
- Check OpenAI API key is set
- Verify internet access for PDF/YouTube
- Check logs for specific errors

### Frontend Can't Connect
- Verify CORS settings
- Check backend URL is correct
- Ensure backend is running

## 🎉 Success!

Once deployed, your app will be live at:
- **Backend**: `https://your-app.railway.app`
- **Frontend**: `https://your-frontend.vercel.app` (if using Vercel)

Test the health endpoint: `https://your-app.railway.app/api/health`

