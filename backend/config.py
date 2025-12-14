"""
Configuration module for the AI Study Tool.
Allows easy switching between providers and models.
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Database
    DATABASE_URL = os.getenv(
        'DATABASE_URL',
        'sqlite:///study_tool.db'
    )
    # SQLAlchemy expects SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # LLM Provider (openai or gemini)
    LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'openai')
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')
    OPENAI_EMBEDDING_MODEL = os.getenv('OPENAI_EMBEDDING_MODEL', 'text-embedding-3-small')
    
    # Gemini
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-pro')
    
    # RAG Settings
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', '1000'))
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', '200'))
    TOP_K_RESULTS = int(os.getenv('TOP_K_RESULTS', '5'))
    SIMILARITY_THRESHOLD = float(os.getenv('SIMILARITY_THRESHOLD', '0.7'))
    
    # Audio Settings
    TTS_PROVIDER = os.getenv('TTS_PROVIDER', 'openai')
    TEACHER_VOICE = os.getenv('TEACHER_VOICE', 'alloy')
    STUDENT_VOICE = os.getenv('STUDENT_VOICE', 'nova')
    
    # Video Settings
    VIDEO_OUTPUT_DIR = os.getenv('VIDEO_OUTPUT_DIR', 'backend/static/videos')
    AUDIO_OUTPUT_DIR = os.getenv('AUDIO_OUTPUT_DIR', 'backend/static/audio')
    
    # Content Sources
    PDF_URL = 'https://drive.google.com/file/d/1K9tjpEljoDnYXwW1y4jt_gxW1753lxBW/view'
    YOUTUBE_VIDEOS = [
        'https://youtu.be/Ec19ljjvlCI',
        'https://www.youtube.com/watch?v=Z_S0VA4jKes'
    ]
    
    # System Prompts
    TEACHER_SYSTEM_PROMPT = """You are an experienced economics teacher. Your role is to:
- Explain concepts clearly and structured
- Use examples and analogies
- Break down complex ideas into digestible parts
- Answer questions based ONLY on the provided context
- If information is not in the context, say "I don't have that information in the provided materials"
- Always cite your sources (PDF or Video)"""
    
    STUDENT_SYSTEM_PROMPT = """You are a curious economics student. Your role is to:
- Ask follow-up questions
- Request clarification
- Show curiosity about concepts
- Ask "why" and "how" questions
- Keep questions concise and natural"""
    
    CHAT_SYSTEM_PROMPT = """You are an AI economics tutor. Your role is to:
- Answer questions based ONLY on the provided context from PDF and videos
- Cite sources (PDF or Video) for every answer
- Refuse to answer if information is not in the materials
- Provide clear, educational explanations
- For exam mode: use bullet points and concise answers
- For simple mode: explain like the student is 12 years old"""

