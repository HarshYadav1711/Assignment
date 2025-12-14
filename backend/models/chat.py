"""
Chat-related database models.
"""
import uuid
from datetime import datetime
from backend.models import db

class ChatSession(db.Model):
    """Represents a chat session"""
    __tablename__ = 'chat_sessions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    messages = db.relationship('ChatMessage', backref='session', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'message_count': len(self.messages)
        }

class ChatMessage(db.Model):
    """Represents a chat message"""
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), db.ForeignKey('chat_sessions.id'), nullable=False)
    user_message = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)
    sources = db.Column(db.Text)  # Comma-separated list of sources
    mode = db.Column(db.String(20), default='normal')  # normal, exam, simple
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'user_message': self.user_message,
            'ai_response': self.ai_response,
            'sources': self.sources.split(',') if self.sources else [],
            'mode': self.mode,
            'created_at': self.created_at.isoformat()
        }

