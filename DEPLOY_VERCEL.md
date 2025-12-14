# 🚀 Deploying to Vercel - Step by Step

## ⚠️ Important: Vercel Limitations

Vercel is **serverless-only**, which means:
- ❌ No persistent file storage (use Cloudinary/S3)
- ❌ No SQLite (use external database)
- ❌ No long-running processes (RAG initialization needs rework)
- ❌ Limited execution time (60s max for free tier)

## 🎯 Recommended: Use Railway Instead

For this Flask + React app, **Railway** is much easier:
- ✅ Full Flask app support
- ✅ Built-in PostgreSQL
- ✅ Persistent storage
- ✅ No serverless limitations

**See `DEPLOY_RAILWAY.md` for Railway deployment (recommended)**

---

## 📋 If You Still Want Vercel

### Prerequisites

1. **External Database**: Set up PlanetScale, Supabase, or MongoDB Atlas
2. **File Storage**: Set up Cloudinary (free tier available)
3. **Vector DB**: Set up Pinecone (free tier available)
4. **Vercel Account**: https://vercel.com

### Step 1: Restructure for Serverless

The current Flask app needs significant changes:

1. **Convert to serverless functions**: Each route becomes a function
2. **Remove FAISS**: Use Pinecone for vector search
3. **Remove file storage**: Use Cloudinary
4. **Update RAG engine**: Use Pinecone instead of FAISS

### Step 2: Set Up External Services

#### A. Database (PlanetScale - Recommended)

```bash
# 1. Sign up: https://planetscale.com
# 2. Create database
# 3. Get connection string
# 4. Update DATABASE_URL in Vercel env vars
```

#### B. File Storage (Cloudinary)

```bash
# 1. Sign up: https://cloudinary.com
# 2. Get API credentials
# 3. Add to Vercel env vars:
#    CLOUDINARY_URL=cloudinary://...
```

#### C. Vector Database (Pinecone)

```bash
# 1. Sign up: https://www.pinecone.io
# 2. Create index
# 3. Get API key
# 4. Add to Vercel env vars:
#    PINECONE_API_KEY=...
#    PINECONE_ENVIRONMENT=...
```

### Step 3: Update Code for Serverless

Major changes needed:

1. **Replace FAISS with Pinecone** in `rag_engine.py`
2. **Replace file storage** with Cloudinary in `audio_service.py` and `video_service.py`
3. **Convert Flask routes** to serverless functions
4. **Remove long-running initialization** (RAG init must be per-request or cached)

### Step 4: Configure Vercel

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login**:
   ```bash
   vercel login
   ```

3. **Link project**:
   ```bash
   vercel link
   ```

4. **Set environment variables**:
   ```bash
   vercel env add OPENAI_API_KEY
   vercel env add DATABASE_URL
   vercel env add CLOUDINARY_URL
   vercel env add PINECONE_API_KEY
   vercel env add PINECONE_ENVIRONMENT
   ```

### Step 5: Build Frontend

```bash
cd frontend
npm run build
```

### Step 6: Deploy

```bash
vercel --prod
```

## 🔄 Alternative: Hybrid Deployment (Easier)

**Deploy frontend to Vercel, backend elsewhere:**

1. **Frontend → Vercel**:
   - Build React app
   - Deploy as static site
   - Update API URLs to point to backend

2. **Backend → Railway/Render**:
   - Deploy Flask app normally
   - Use their database
   - Use their storage

This is **much simpler** and recommended!

## 📝 Quick Railway Deployment (Recommended)

Railway is perfect for this project:

```bash
# 1. Install Railway CLI
npm i -g @railway/cli

# 2. Login
railway login

# 3. Initialize
railway init

# 4. Add PostgreSQL
railway add postgresql

# 5. Deploy
railway up
```

See `DEPLOY_RAILWAY.md` for detailed Railway guide.

## 🎯 Recommendation

**For this project, use Railway instead of Vercel:**
- ✅ Easier setup
- ✅ No code restructuring needed
- ✅ Better for Flask apps
- ✅ Built-in database
- ✅ Persistent storage
- ✅ Free tier available

Would you like me to create a Railway deployment guide instead?

