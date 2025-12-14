"""
Content source database models.
Stores user-uploaded PDFs and YouTube video URLs.
"""
import uuid
from datetime import datetime
from backend.models import db

class ContentSource(db.Model):
    """Represents a content source (PDF or YouTube video)"""
    __tablename__ = 'content_sources'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_type = db.Column(db.String(20), nullable=False)  # 'pdf_url', 'pdf_file', 'youtube'
    source_url = db.Column(db.Text)  # URL for PDF or YouTube
    file_path = db.Column(db.Text)  # Local file path for uploaded PDFs
    title = db.Column(db.String(255))  # User-friendly title
    description = db.Column(db.Text)  # Optional description
    is_active = db.Column(db.Boolean, default=True)  # Can be disabled without deleting
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'source_type': self.source_type,
            'source_url': self.source_url,
            'file_path': self.file_path,
            'title': self.title,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

