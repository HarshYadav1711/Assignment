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

from backend.config import Config
from backend.services.llm_service import LLMService
from backend.services.rag_engine import RAGEngine
from backend.services.audio_service import AudioService
from backend.services.video_service import VideoService
from backend.models import db
from backend.models.chat import ChatSession, ChatMessage

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
                rag_engine.initialize()
                logger.info("RAG engine initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize RAG engine: {e}")
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
        context_chunks = rag.search(message, top_k=Config.TOP_K_RESULTS)
        
        if not context_chunks:
            return jsonify({
                'response': "I don't have relevant information about that topic in the provided materials.",
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
        chat_message = ChatMessage(
            session_id=session_id,
            user_message=message,
            ai_response=response,
            sources=','.join(sources),
            mode=mode
        )
        db.session.add(chat_message)
        db.session.commit()
        
        return jsonify({
            'response': response,
            'sources': sources,
            'session_id': session_id
        })
    
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({'error': str(e)}), 500

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

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)

