# 🔥 Interactive AI Study Tool - Economics Chapter

A production-ready interactive study platform inspired by NotebookLLM, featuring AI-powered Q&A, two-person audio dialogue, and video summaries.

## 🎯 Features

- **Interactive Q&A**: Context-aware chat grounded in PDF and YouTube video content
- **Audio Dialogue Mode**: Two-person conversation simulation (Teacher ↔ Student) with TTS
- **Video Summaries**: AI-generated explainer videos for concepts and exam tips
- **Source Citations**: Every answer cites its source (PDF/Video)
- **Exam Mode**: Toggle for bullet-pointed, exam-oriented responses

## 🏗️ Architecture

```
Assignment/
├── backend/              # Flask API server
│   ├── app.py           # Main Flask application
│   ├── services/        # Modular service layer
│   │   ├── llm_service.py
│   │   ├── rag_engine.py
│   │   ├── audio_service.py
│   │   └── video_service.py
│   ├── models/          # Database models
│   ├── utils/           # Helper functions
│   └── config.py        # Configuration
├── frontend/            # React application
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── App.jsx
│   └── package.json
└── requirements.txt     # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- MySQL 8.0+ (or use SQLite for development)
- OpenAI API key (or Gemini API key)

### Automated Setup

```bash
# Run the setup script (recommended)
python setup.py
```

### Manual Setup

#### Backend Setup

#### Windows Users (Important!)
If you encounter Pillow or faiss-cpu installation errors, see `QUICK_FIX_WINDOWS.md` first!

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip first (recommended)
python -m pip install --upgrade pip setuptools wheel

# Install dependencies
# On Windows, you may need to install Pillow separately first:
# pip install Pillow --only-binary :all:
pip install -r requirements.txt

# Copy environment file
cp .env.example .env  # On Windows: copy .env.example .env
# Edit .env and add your API keys

# Set up database
python backend/scripts/setup_db.py

# Start Flask server
cd backend
python app.py
```

#### Frontend Setup

```bash
cd frontend
npm install
npm start
```

The application will be available at `http://localhost:3000`

### Environment Variables

Create a `.env` file in the root directory with:

```env
OPENAI_API_KEY=your_key_here
DATABASE_URL=mysql+pymysql://user:password@localhost/study_tool
```

See `.env.example` for all available options.

## 📚 Content Sources

The AI is grounded in:
1. Economics Chapter PDF (Google Drive)
2. YouTube Video 1: https://youtu.be/Ec19ljjvlCI
3. YouTube Video 2: https://www.youtube.com/watch?v=Z_S0VA4jKes

## 🧠 Design Decisions

### RAG Pipeline
- **Chunking Strategy**: Semantic chunking with overlap to preserve context
- **Embeddings**: OpenAI `text-embedding-3-small` for cost efficiency
- **Vector Store**: In-memory FAISS for MVP, easily swappable to Pinecone/Weaviate

### LLM Service
- **Model**: GPT-4 Turbo for quality, with fallback to GPT-3.5
- **Prompt Engineering**: Strict system prompts to prevent hallucination
- **Context Window**: 8K tokens for comprehensive context

### Audio Dialogue
- **TTS**: OpenAI TTS API with distinct voice profiles
- **Turn Management**: State machine for conversation flow
- **Streaming**: WebSocket for real-time audio delivery

### Video Summaries
- **Generation**: Slides + voice-over approach for speed
- **Storage**: Local filesystem with CDN-ready structure
- **Caching**: Pre-generate common topics for instant playback

## 🔧 Configuration

Edit `backend/config.py` to:
- Switch LLM providers (OpenAI ↔ Gemini)
- Adjust chunk sizes and overlap
- Configure TTS voices
- Set database connection

## 📦 Production Deployment

1. Set up MySQL database
2. Configure environment variables
3. Run database migrations
4. Build frontend: `npm run build`
5. Serve with Gunicorn: `gunicorn -w 4 app:app`

## 🎓 Future Enhancements

- Multi-chapter support
- User authentication
- Progress tracking
- Collaborative study rooms
- Mobile app

## 📝 License

MIT License - Built for internship evaluation

