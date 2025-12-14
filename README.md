# 🔥 Interactive AI Study Tool - Universal Learning Platform

A production-ready interactive study platform inspired by NotebookLLM, featuring AI-powered Q&A, two-person audio dialogue, and video summaries. Works with **any subject or domain** - just provide your own study materials!

## 🎯 Features

- **Interactive Q&A**: Context-aware chat grounded in your PDF and YouTube video content
- **Audio Dialogue Mode**: Two-person conversation simulation (Teacher ↔ Student) with TTS
- **Video Summaries**: AI-generated explainer videos for concepts and exam tips
- **Source Citations**: Every answer cites its source (PDF/Video)
- **Exam Mode**: Toggle for bullet-pointed, exam-oriented responses
- **Universal Support**: Works with any subject - Math, Science, History, Literature, Programming, etc.

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

# Start Flask server (from project root)
python run_backend.py
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

# Your study materials (see CONTENT_SETUP.md)
PDF_URLS=https://drive.google.com/file/d/YOUR_PDF_ID/view
YOUTUBE_VIDEOS=https://youtu.be/VIDEO_ID_1,https://youtu.be/VIDEO_ID_2
```

See `.env.example` for all available options.

## 📚 Content Sources

The AI is grounded in **your own study materials**. Configure via environment variables:

### Setting Up Your Content

1. **PDF Documents**: Add PDF URLs to `.env`:
   ```env
   PDF_URLS=https://drive.google.com/file/d/YOUR_PDF_ID/view,https://another-pdf-url.com/file.pdf
   ```

2. **YouTube Videos**: Add video URLs to `.env`:
   ```env
   YOUTUBE_VIDEOS=https://youtu.be/VIDEO_ID_1,https://www.youtube.com/watch?v=VIDEO_ID_2
   ```

3. **Optional - Subject Name** (for customization):
   ```env
   SUBJECT_NAME=Physics
   ```

The tool works with **any subject**: Math, Science, History, Literature, Programming, etc. Just provide your own materials!

**See `CONTENT_SETUP.md` for detailed instructions.**

## 🧠 Design Decisions

### Universal Subject Support
- **Configurable Content**: Users provide their own PDFs and videos via environment variables
- **Generic Prompts**: System prompts work for any subject or domain
- **Flexible RAG**: Adapts to any type of educational content

### RAG Pipeline
- **Chunking Strategy**: Semantic chunking with overlap to preserve context
- **Embeddings**: OpenAI `text-embedding-3-small` for cost efficiency
- **Vector Store**: In-memory FAISS for MVP, easily swappable to Pinecone/Weaviate
- **Multi-Source Support**: Handles multiple PDFs and videos simultaneously

### LLM Service
- **Model**: GPT-4 Turbo for quality, with fallback to GPT-3.5
- **Prompt Engineering**: Strict system prompts to prevent hallucination
- **Context Window**: 8K tokens for comprehensive context
- **Subject-Agnostic**: Works with any domain or field of study

### Audio Dialogue
- **TTS**: OpenAI TTS API with distinct voice profiles
- **Turn Management**: State machine for conversation flow
- **Streaming**: WebSocket for real-time audio delivery

### Video Summaries
- **Generation**: Slides + voice-over approach for speed
- **Storage**: Local filesystem with CDN-ready structure
- **Caching**: Pre-generate common topics for instant playback

## 🔧 Configuration

Edit `backend/config.py` or `.env` file to:
- Switch LLM providers (OpenAI ↔ Gemini)
- Adjust chunk sizes and overlap
- Configure TTS voices
- Set database connection
- **Add your own study materials** (PDFs and videos)

## 📦 Production Deployment

1. Set up MySQL database
2. Configure environment variables
3. Run database migrations
4. Build frontend: `npm run build`
5. Serve with Gunicorn: `gunicorn -w 4 app:app`

See `DEPLOY_RAILWAY.md` for Railway deployment guide.

## 🎓 Future Enhancements

- Multi-chapter/subject support with organization
- User authentication and personal study libraries
- Progress tracking across subjects
- Collaborative study rooms
- Mobile app
- Direct file upload (beyond URLs)
- Support for more content types (docx, pptx, etc.)

## 📝 License

MIT License - Built for internship evaluation
