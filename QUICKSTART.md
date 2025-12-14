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

1. Copy `.env.example` to `.env`
2. Add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```
3. Configure database (or use SQLite for testing):
   ```
   DATABASE_URL=sqlite:///study_tool.db
   ```

### Step 3: Initialize Database

```bash
python backend/scripts/setup_db.py
```

### Step 4: Start Backend

```bash
cd backend
python app.py
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

1. **Wait for RAG initialization**: The backend will automatically ingest the PDF and YouTube videos on first start (this may take 1-2 minutes)

2. **Try the Chat**:
   - Go to the Chat tab
   - Ask: "What is supply and demand?"
   - See source citations below the answer

3. **Try Audio Dialogue**:
   - Go to Audio Dialogue tab
   - Enter a topic: "market equilibrium"
   - Click "Start Dialogue"
   - Listen to the teacher-student conversation

4. **Generate a Video**:
   - Go to Video Summaries tab
   - Enter a topic: "inflation"
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

- Read `ARCHITECTURE.md` for system design details
- Check `README.md` for full documentation
- Customize prompts in `backend/config.py`
- Add more content sources by editing `backend/config.py`

