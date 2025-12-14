# Architecture Documentation

## System Overview

The AI Study Tool is a full-stack application built with Flask (backend) and React (frontend), designed to provide an interactive learning experience for students studying any subject or domain using RAG (Retrieval Augmented Generation) and LLM technologies. Users provide their own study materials (PDFs, videos), and the tool creates a personalized knowledge base.

## Architecture Layers

### 1. Frontend Layer (React)

**Location**: `frontend/`

**Components**:
- `App.jsx`: Main application container with tab navigation
- `ChatPanel.jsx`: Interactive Q&A interface with mode selection
- `AudioDialoguePanel.jsx`: Two-person dialogue interface
- `VideoGallery.jsx`: Video summary gallery and generator
- `Header.jsx`: Application header

**Key Features**:
- Mode selection (Normal, Exam, Simple)
- Real-time chat with source citations
- Audio dialogue controls
- Video generation and playback

**State Management**: React hooks (useState, useEffect)

### 2. API Layer (Flask)

**Location**: `backend/app.py`

**Endpoints**:
- `GET /api/health`: Health check
- `POST /api/chat`: Chat Q&A
- `POST /api/audio/dialogue`: Start audio dialogue
- `POST /api/audio/dialogue/<id>/next`: Continue dialogue
- `GET /api/audio/<id>`: Get audio file
- `GET /api/video/summaries`: List video summaries
- `POST /api/video/generate`: Generate video
- `GET /api/video/<id>`: Get video file
- `POST /api/ingest`: Re-ingest content

**Design Pattern**: RESTful API with JSON responses

### 3. Service Layer

**Location**: `backend/services/`

#### LLM Service (`llm_service.py`)
- **Purpose**: Abstract LLM provider (OpenAI/Gemini)
- **Key Methods**:
  - `generate_response()`: Generate text responses
  - `generate_embeddings()`: Create vector embeddings
- **Design**: Provider abstraction allows easy model switching

#### RAG Engine (`rag_engine.py`)
- **Purpose**: Retrieval Augmented Generation pipeline
- **Components**:
  - Content ingestion (PDF + YouTube)
  - Text chunking with overlap
  - Vector embedding generation
  - FAISS vector search
- **Key Methods**:
  - `initialize()`: Ingest and vectorize all content
  - `search()`: Semantic search for relevant chunks

#### Audio Service (`audio_service.py`)
- **Purpose**: Two-person dialogue generation
- **Features**:
  - Turn-based conversation flow
  - TTS generation with distinct voices
  - Dialogue state management
- **Key Methods**:
  - `create_dialogue()`: Start new dialogue
  - `continue_dialogue()`: Generate next turn
  - `_generate_audio()`: Create TTS audio files

#### Video Service (`video_service.py`)
- **Purpose**: AI video summary generation
- **Pipeline**:
  1. Generate script using LLM
  2. Create image slides
  3. Generate narration audio
  4. Combine into video
- **Key Methods**:
  - `generate_summary()`: Full video generation pipeline
  - `_create_slides()`: Generate slide images
  - `_create_video()`: Combine slides and audio

### 4. Data Layer

**Location**: `backend/models/`

#### Database Models
- `ChatSession`: Chat conversation sessions
- `ChatMessage`: Individual messages with sources and mode

**Database**: MySQL (configurable via SQLAlchemy)

### 5. Utility Layer

**Location**: `backend/utils/`

- `pdf_extractor.py`: PDF text extraction from Google Drive
- `youtube_extractor.py`: YouTube transcript fetching
- `text_chunker.py`: Semantic text chunking with overlap

## Data Flow

### Chat Flow
1. User sends message → Frontend
2. Frontend → API `/api/chat`
3. API → RAG Engine: Search for relevant context
4. API → LLM Service: Generate response with context
5. API → Database: Save message
6. API → Frontend: Return response with sources

### Audio Dialogue Flow
1. User enters topic → Frontend
2. Frontend → API `/api/audio/dialogue`
3. API → RAG Engine: Get topic context
4. API → LLM Service: Generate teacher explanation
5. API → LLM Service: Generate student question
6. API → Audio Service: Generate TTS for both
7. API → Frontend: Return dialogue with audio URLs

### Video Generation Flow
1. User requests video → Frontend
2. Frontend → API `/api/video/generate`
3. API → RAG Engine: Get topic content
4. API → LLM Service: Generate script
5. API → Video Service: Create slides
6. API → Audio Service: Generate narration
7. API → Video Service: Combine into video
8. API → Frontend: Return video URL

## RAG Pipeline Details

### Content Ingestion
1. **PDF Extraction**:
   - Download from Google Drive
   - Extract text per page
   - Chunk with overlap

2. **YouTube Transcripts**:
   - Extract video ID from URL
   - Fetch transcript via API
   - Format as continuous text
   - Chunk with overlap

### Vectorization
- **Embedding Model**: OpenAI `text-embedding-3-small` (1536 dimensions)
- **Vector Store**: FAISS (L2 distance)
- **Chunking**: 1000 chars with 200 char overlap

### Search Process
1. Generate query embedding
2. Search FAISS index (top-k)
3. Filter by similarity threshold (0.7)
4. Return chunks with metadata

## Configuration

**Location**: `backend/config.py`

**Key Settings**:
- LLM provider selection (OpenAI/Gemini)
- Chunk size and overlap
- Similarity threshold
- TTS voice selection
- System prompts

**Environment Variables**: `.env` file

## Error Handling

- **API Level**: Try-catch with JSON error responses
- **Service Level**: Logging with graceful degradation
- **Frontend Level**: User-friendly error messages

## Security Considerations

- API keys stored in environment variables
- CORS configured for frontend origin
- Input validation on API endpoints
- SQL injection prevention via SQLAlchemy ORM

## Scalability Considerations

### Current Limitations
- In-memory dialogue storage (not persistent)
- In-memory video summaries (not persistent)
- FAISS index in memory (not persisted)

### Future Improvements
- Redis for dialogue state
- Database for video metadata
- Persistent FAISS index with periodic updates
- CDN for media file delivery
- Caching layer for common queries

## Performance Optimizations

1. **Lazy Service Initialization**: Services created on first use
2. **Chunking Strategy**: Overlap preserves context boundaries
3. **Vector Search**: FAISS for fast similarity search
4. **Caching**: Consider caching common queries

## Testing Strategy

### Unit Tests (Future)
- Service layer methods
- Utility functions
- Model serialization

### Integration Tests (Future)
- API endpoint testing
- RAG pipeline testing
- End-to-end flows

## Deployment

### Development
- Flask dev server
- React dev server with proxy

### Production
- Gunicorn for Flask
- Nginx for static files
- React build served statically
- MySQL database
- Environment-based configuration

## Monitoring & Logging

- Python logging module
- Log levels: INFO, ERROR
- Structured logging for debugging

## Future Enhancements

1. **Multi-chapter Support**: Extend RAG to multiple chapters
2. **User Authentication**: Add user accounts
3. **Progress Tracking**: Track learning progress
4. **Collaborative Features**: Study groups
5. **Mobile App**: React Native version
6. **Advanced Analytics**: Learning insights

