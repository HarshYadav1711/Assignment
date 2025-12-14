"""
Main Flask application for the AI Study Tool.
Provides REST API endpoints for chat, audio, video, and content ingestion.
"""
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import logging
import uuid

from backend.config import Config
from backend.services.llm_service import LLMService
from backend.services.rag_engine import RAGEngine
from backend.services.audio_service import AudioService
from backend.services.video_service import VideoService
from backend.models import db
from backend.models.chat import ChatSession, ChatMessage
from backend.models.content import ContentSource

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)
# Ensure SQLALCHEMY_DATABASE_URI is set
if not app.config.get('SQLALCHEMY_DATABASE_URI'):
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
CORS(app)

# Initialize database
db.init_app(app)

# Initialize services (lazy initialization)
llm_service = None
rag_engine = None
audio_service = None
video_service = None

def get_llm_service():
    global llm_service
    if llm_service is None:
        llm_service = LLMService()
    return llm_service

def get_rag_engine():
    global rag_engine
    if rag_engine is None:
        rag_engine = RAGEngine()
        if not rag_engine.is_initialized:
            try:
                with app.app_context():
                    rag_engine.initialize()
                logger.info("RAG engine initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize RAG engine: {e}")
                # Mark as initialized even if empty to prevent repeated errors
                rag_engine.is_initialized = True
                rag_engine.chunks = []
                rag_engine.index = None
    return rag_engine

def get_audio_service():
    global audio_service
    if audio_service is None:
        audio_service = AudioService()
    return audio_service

def get_video_service():
    global video_service
    if video_service is None:
        video_service = VideoService()
    return video_service

# Create tables
with app.app_context():
    db.create_all()
    # Create upload directories
    os.makedirs('backend/static/uploads/pdfs', exist_ok=True)

@app.route('/', methods=['GET'])
def root():
    """Root endpoint - API information"""
    return jsonify({
        'message': 'AI Study Tool API',
        'status': 'running',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health',
            'chat': '/api/chat',
            'content_sources': '/api/content/sources',
            'audio_dialogue': '/api/audio/dialogue',
            'video_summaries': '/api/video/summaries'
        },
        'docs': 'This is the backend API. The frontend should be deployed separately.'
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    rag = get_rag_engine()
    return jsonify({
        'status': 'healthy',
        'rag_initialized': rag.is_initialized if rag else False
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Chat endpoint for Q&A interactions.
    Expects: { "message": "...", "session_id": "...", "mode": "normal|exam|simple" }
    Returns: { "response": "...", "sources": [...], "session_id": "..." }
    """
    try:
        data = request.json
        message = data.get('message', '')
        session_id = data.get('session_id')
        mode = data.get('mode', 'normal')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Create or get session
        if not session_id:
            session = ChatSession()
            db.session.add(session)
            db.session.commit()
            session_id = session.id
        else:
            session = ChatSession.query.get(session_id)
            if not session:
                return jsonify({'error': 'Invalid session_id'}), 404
        
        # Retrieve relevant context using RAG
        rag = get_rag_engine()
        
        # Check if RAG is initialized
        if not rag.is_initialized:
            return jsonify({
                'response': "I'm still processing your study materials. Please add some PDFs or YouTube videos in the 'My Materials' tab, then try again in a moment.",
                'sources': [],
                'session_id': session_id
            })
        
        # Try to search for relevant context
        try:
            context_chunks = rag.search(message, top_k=Config.TOP_K_RESULTS)
        except Exception as e:
            logger.warning(f"RAG search error: {e}")
            context_chunks = []
        
        if not context_chunks:
            return jsonify({
                'response': "I don't have relevant information about that topic in your study materials. Please make sure you've added PDFs or YouTube videos in the 'My Materials' tab, or try asking about topics covered in your materials.",
                'sources': [],
                'session_id': session_id
            })
        
        # Build context string
        context = "\n\n".join([
            f"[Source: {chunk['source']}]\n{chunk['text']}"
            for chunk in context_chunks
        ])
        
        # Get sources for citation
        sources = list(set([chunk['source'] for chunk in context_chunks]))
        
        # Generate response using LLM
        try:
            llm = get_llm_service()
            system_prompt = Config.CHAT_SYSTEM_PROMPT
            if mode == 'exam':
                system_prompt += "\n\nFormat your response as bullet points suitable for exam answers."
            elif mode == 'simple':
                system_prompt += "\n\nExplain in simple terms, as if the student is 12 years old."
            
            response = llm.generate_response(
                system_prompt=system_prompt,
                user_message=message,
                context=context
            )
            
            # Save message to database
            try:
                chat_message = ChatMessage(
                    session_id=session_id,
                    user_message=message,
                    ai_response=response,
                    sources=','.join(sources),
                    mode=mode
                )
                db.session.add(chat_message)
                db.session.commit()
            except Exception as db_error:
                logger.warning(f"Failed to save message to database: {db_error}")
                # Continue even if DB save fails
            
            return jsonify({
                'response': response,
                'sources': sources,
                'session_id': session_id
            })
        except Exception as llm_error:
            logger.error(f"LLM service error: {llm_error}")
            # Return a helpful message instead of crashing
            return jsonify({
                'response': "I encountered an error while processing your question. This might be because: (1) I don't have relevant information about that topic in your study materials, (2) there was a temporary issue with the AI service. Please try asking about topics covered in your PDFs or videos, or try again in a moment.",
                'sources': [],
                'session_id': session_id
            })
    
    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        # Return a user-friendly error message (always return 200 with response field)
        session_id_local = session_id if 'session_id' in locals() else None
        if not session_id_local:
            try:
                session = ChatSession()
                db.session.add(session)
                db.session.commit()
                session_id_local = session.id
            except:
                pass
        
        return jsonify({
            'response': "I don't have relevant information about that topic in your study materials. Please make sure you've added PDFs or YouTube videos in the 'My Materials' tab, or try asking about topics covered in your materials.",
            'sources': [],
            'session_id': session_id_local
        })

@app.route('/api/audio/dialogue', methods=['POST'])
def start_dialogue():
    """
    Start a two-person audio dialogue.
    Expects: { "topic": "...", "session_id": "..." }
    Returns: { "dialogue_id": "...", "initial_message": "..." }
    """
    try:
        data = request.json
        topic = data.get('topic', 'general concepts')
        session_id = data.get('session_id')
        
        # Get context for topic
        rag = get_rag_engine()
        context_chunks = rag.search(topic, top_k=3)
        context = "\n\n".join([
            f"[Source: {chunk['source']}]\n{chunk['text']}"
            for chunk in context_chunks
        ])
        
        # Generate initial teacher explanation
        llm = get_llm_service()
        teacher_prompt = f"{Config.TEACHER_SYSTEM_PROMPT}\n\nExplain: {topic}"
        teacher_message = llm.generate_response(
            system_prompt=teacher_prompt,
            user_message=f"Explain {topic} based on the context.",
            context=context
        )
        
        # Generate student follow-up question
        student_prompt = f"{Config.STUDENT_SYSTEM_PROMPT}\n\nTeacher just explained: {teacher_message[:200]}..."
        student_message = llm.generate_response(
            system_prompt=student_prompt,
            user_message="Ask a natural follow-up question.",
            context=""
        )
        
        audio = get_audio_service()
        dialogue_id = audio.create_dialogue(
            topic=topic,
            teacher_message=teacher_message,
            student_message=student_message,
            session_id=session_id
        )
        
        return jsonify({
            'dialogue_id': dialogue_id,
            'initial_message': teacher_message,
            'student_question': student_message
        })
    
    except Exception as e:
        logger.error(f"Dialogue error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/audio/dialogue/<dialogue_id>/next', methods=['POST'])
def continue_dialogue(dialogue_id):
    """
    Continue the dialogue with next turn.
    Returns: { "speaker": "teacher|student", "message": "...", "audio_url": "..." }
    """
    try:
        data = request.json
        user_question = data.get('user_question')  # Optional user intervention
        
        audio = get_audio_service()
        result = audio.continue_dialogue(dialogue_id, user_question)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Continue dialogue error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/audio/<audio_id>', methods=['GET'])
def get_audio(audio_id):
    """Get generated audio file"""
    try:
        audio = get_audio_service()
        audio_path = audio.get_audio_path(audio_id)
        if os.path.exists(audio_path):
            return send_file(audio_path, mimetype='audio/mpeg')
        return jsonify({'error': 'Audio not found'}), 404
    except Exception as e:
        logger.error(f"Get audio error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/video/summaries', methods=['GET'])
def list_video_summaries():
    """List available video summaries"""
    try:
        video = get_video_service()
        summaries = video.list_summaries()
        return jsonify({'summaries': summaries})
    except Exception as e:
        logger.error(f"List summaries error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/video/generate', methods=['POST'])
def generate_video():
    """
    Generate a video summary for a topic.
    Expects: { "topic": "...", "type": "concept|exam_tips|definition" }
    Returns: { "video_id": "...", "video_url": "..." }
    """
    try:
        data = request.json
        topic = data.get('topic', '')
        video_type = data.get('type', 'concept')
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        # Get context for topic
        rag = get_rag_engine()
        context_chunks = rag.search(topic, top_k=5)
        context = "\n\n".join([chunk['text'] for chunk in context_chunks])
        
        video = get_video_service()
        video_id, video_url = video.generate_summary(
            topic=topic,
            content=context,
            video_type=video_type
        )
        
        return jsonify({
            'video_id': video_id,
            'video_url': video_url
        })
    
    except Exception as e:
        logger.error(f"Generate video error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/video/<video_id>', methods=['GET'])
def get_video(video_id):
    """Get generated video file"""
    try:
        video = get_video_service()
        video_path = video.get_video_path(video_id)
        if os.path.exists(video_path):
            return send_file(video_path, mimetype='video/mp4')
        return jsonify({'error': 'Video not found'}), 404
    except Exception as e:
        logger.error(f"Get video error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/ingest', methods=['POST'])
def ingest_content():
    """
    Manually trigger content ingestion.
    Re-initializes RAG engine with PDF and YouTube videos.
    """
    try:
        rag = get_rag_engine()
        # Re-initialize from scratch
        rag.is_initialized = False
        rag.initialize()
        return jsonify({
            'status': 'success',
            'message': 'Content ingested successfully'
        })
    except Exception as e:
        logger.error(f"Ingest error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/sessions', methods=['GET'])
def list_sessions():
    """List all chat sessions"""
    try:
        sessions = ChatSession.query.order_by(ChatSession.created_at.desc()).limit(20).all()
        return jsonify({
            'sessions': [{
                'id': s.id,
                'created_at': s.created_at.isoformat(),
                'message_count': len(s.messages)
            } for s in sessions]
        })
    except Exception as e:
        logger.error(f"List sessions error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/sessions/<session_id>/messages', methods=['GET'])
def get_session_messages(session_id):
    """Get all messages for a session"""
    try:
        session = ChatSession.query.get(session_id)
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        messages = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.created_at).all()
        return jsonify({
            'messages': [{
                'id': m.id,
                'user_message': m.user_message,
                'ai_response': m.ai_response,
                'sources': m.sources.split(',') if m.sources else [],
                'mode': m.mode,
                'created_at': m.created_at.isoformat()
            } for m in messages]
        })
    except Exception as e:
        logger.error(f"Get messages error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/content/sources', methods=['GET'])
def list_content_sources():
    """List all content sources"""
    try:
        sources = ContentSource.query.filter_by(is_active=True).order_by(ContentSource.created_at.desc()).all()
        return jsonify({
            'sources': [s.to_dict() for s in sources]
        })
    except Exception as e:
        logger.error(f"List content sources error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/content/sources', methods=['POST'])
def add_content_source():
    """
    Add a new content source (PDF URL, YouTube URL, or PDF file upload).
    Supports both JSON and form-data for file uploads.
    """
    try:
        # Handle file upload (multipart/form-data)
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            if not file.filename.lower().endswith('.pdf'):
                return jsonify({'error': 'Only PDF files are supported'}), 400
            
            # Save uploaded file
            upload_dir = os.path.join('backend', 'static', 'uploads', 'pdfs')
            os.makedirs(upload_dir, exist_ok=True)
            
            filename = f"{uuid.uuid4()}_{file.filename}"
            file_path = os.path.join(upload_dir, filename)
            file.save(file_path)
            
            source = ContentSource(
                source_type='pdf_file',
                file_path=file_path,
                title=request.form.get('title', file.filename),
                description=request.form.get('description', '')
            )
        else:
            # Handle URL-based sources (JSON)
            data = request.json
            source_type = data.get('type') or data.get('source_type')
            
            if not source_type:
                return jsonify({'error': 'Source type is required'}), 400
            
            if source_type not in ['pdf_url', 'youtube']:
                return jsonify({'error': f'Invalid source type: {source_type}'}), 400
            
            url = data.get('url') or data.get('source_url')
            if not url:
                return jsonify({'error': 'URL is required'}), 400
            
            source = ContentSource(
                source_type=source_type,
                source_url=url,
                title=data.get('title', url),
                description=data.get('description', '')
            )
        
        db.session.add(source)
        db.session.commit()
        
        # Trigger re-ingestion in background (don't block response)
        try:
            rag = get_rag_engine()
            rag.is_initialized = False
            # Initialize in background to avoid blocking
            # Pass app context to background thread
            import threading
            def reinitialize_with_context():
                with app.app_context():
                    rag.initialize()
            threading.Thread(target=reinitialize_with_context, daemon=True).start()
        except Exception as e:
            logger.warning(f"Failed to trigger re-ingestion: {e}")
        
        return jsonify({
            'message': 'Content source added successfully. Processing in background...',
            'source': source.to_dict()
        })
    
    except Exception as e:
        logger.error(f"Add content source error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/content/sources/<source_id>', methods=['DELETE'])
def delete_content_source(source_id):
    """Delete or deactivate a content source"""
    try:
        source = ContentSource.query.get(source_id)
        if not source:
            return jsonify({'error': 'Source not found'}), 404
        
        # Soft delete (deactivate)
        source.is_active = False
        db.session.commit()
        
        # Trigger re-ingestion in background
        try:
            rag = get_rag_engine()
            rag.is_initialized = False
            import threading
            def reinitialize_with_context():
                with app.app_context():
                    rag.initialize()
            threading.Thread(target=reinitialize_with_context, daemon=True).start()
        except Exception as e:
            logger.warning(f"Failed to trigger re-ingestion: {e}")
        
        return jsonify({'message': 'Content source deleted successfully'})
    
    except Exception as e:
        logger.error(f"Delete content source error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/content/upload', methods=['POST'])
def upload_pdf():
    """Upload a PDF file directly"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Only PDF files are supported'}), 400
        
        # Check file size (50MB limit)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        if file_size > 50 * 1024 * 1024:
            return jsonify({'error': 'File size must be less than 50MB'}), 400
        
        # Save file
        upload_dir = os.path.join('backend', 'static', 'uploads', 'pdfs')
        os.makedirs(upload_dir, exist_ok=True)
        
        filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)
        
        # Create content source record
        source = ContentSource(
            source_type='pdf_file',
            file_path=file_path,
            title=request.form.get('title', file.filename),
            description=request.form.get('description', '')
        )
        
        db.session.add(source)
        db.session.commit()
        
        # Trigger re-ingestion in background
        try:
            rag = get_rag_engine()
            rag.is_initialized = False
            import threading
            def reinitialize_with_context():
                with app.app_context():
                    rag.initialize()
            threading.Thread(target=reinitialize_with_context, daemon=True).start()
        except Exception as e:
            logger.warning(f"Failed to trigger re-ingestion: {e}")
        
        return jsonify({
            'message': 'PDF uploaded successfully. Processing in background...',
            'source': source.to_dict()
        })
    
    except Exception as e:
        logger.error(f"Upload PDF error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)

