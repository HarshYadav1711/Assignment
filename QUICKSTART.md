# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies
cd frontend
npm install
cd ..
```

### Step 2: Configure Environment

1. **Copy `.env.example` to `.env`**:
   ```bash
   # On Windows:
   copy .env.example .env
   
   # On Linux/Mac:
   cp .env.example .env
   
   # Or use the helper script:
   python create_env.py
   ```

2. **Edit `.env` and add your OpenAI API key**:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```
   Get your API key from: https://platform.openai.com/api-keys

3. **Database is already configured for SQLite** (good for development):
   ```
   DATABASE_URL=sqlite:///study_tool.db
   ```
   For MySQL, change to:
   ```
   DATABASE_URL=mysql+pymysql://username:password@localhost/study_tool
   ```

### Step 3: Initialize Database

```bash
python backend/scripts/setup_db.py
```

### Step 4: Start Backend

**Option 1: Run from project root (Recommended)**
```bash
# From project root directory
python run_backend.py
```

**Option 2: Run from backend directory**
```bash
cd backend
python -m flask run
# Or: python app.py (if imports are fixed)
```

The backend will start on `http://localhost:5000`

### Step 5: Start Frontend

In a new terminal:

```bash
cd frontend
npm start
```

The frontend will open at `http://localhost:3000`

## 🎯 First Use

1. **Configure your study materials** (see `CONTENT_SETUP.md`):
   - Add PDF URLs to `.env`: `PDF_URLS=url1,url2`
   - Add YouTube video URLs: `YOUTUBE_VIDEOS=url1,url2`
   - Works with any subject: Math, Science, History, Literature, etc.

2. **Wait for RAG initialization**: The backend will automatically ingest your PDFs and YouTube videos on first start (this may take 1-2 minutes)

2. **Try the Chat**:
   - Go to the Chat tab
   - Ask questions about your study materials
   - See source citations below the answer

3. **Try Audio Dialogue**:
   - Go to Audio Dialogue tab
   - Enter a topic from your materials
   - Click "Start Dialogue"
   - Listen to the teacher-student conversation

4. **Generate a Video**:
   - Go to Video Summaries tab
   - Enter a topic from your study materials
   - Select video type
   - Click "Generate Video"

## ⚠️ Troubleshooting

### RAG Engine Not Initializing
- Check your OpenAI API key is set correctly
- Ensure you have internet connection (for PDF/YouTube)
- Check backend logs for specific errors

### Database Connection Error
- For MySQL: Ensure MySQL is running and credentials are correct
- For SQLite: The database file will be created automatically

### Frontend Can't Connect to Backend
- Ensure backend is running on port 5000
- Check CORS settings in `backend/app.py`
- Verify proxy settings in `frontend/package.json`

### Audio/Video Generation Fails
- Ensure OpenAI API key has TTS access
- Check disk space for generated files
- Verify `backend/static/audio` and `backend/static/videos` directories exist

## 📝 Next Steps

- **Set up your study materials**: See `CONTENT_SETUP.md` for detailed instructions
- Read `ARCHITECTURE.md` for system design details
- Check `README.md` for full documentation
- Customize prompts in `backend/config.py` (optional)
- Add more content sources via environment variables

