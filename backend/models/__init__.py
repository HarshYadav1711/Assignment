"""
Database models for the AI Study Tool.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models after db is created
from .chat import ChatSession, ChatMessage
from .content import ContentSource

__all__ = ['db', 'ChatSession', 'ChatMessage', 'ContentSource']
