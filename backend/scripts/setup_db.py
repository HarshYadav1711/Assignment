"""
Database setup script.
Creates tables and optionally seeds initial data.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Load environment variables first
from dotenv import load_dotenv
load_dotenv()

from backend.config import Config
from flask import Flask
from flask_cors import CORS
from backend.models import db
from backend.models.chat import ChatSession, ChatMessage

# Create Flask app with proper configuration
app = Flask(__name__)
app.config.from_object(Config)
# Ensure SQLALCHEMY_DATABASE_URI is set
if not app.config.get('SQLALCHEMY_DATABASE_URI'):
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
CORS(app)

# Initialize database
db.init_app(app)

def setup_database():
    """Create database tables"""
    with app.app_context():
        db.create_all()
        print("[OK] Database tables created successfully")
        
        # Test connection
        try:
            db.session.execute(db.text("SELECT 1"))
            print("[OK] Database connection successful")
        except Exception as e:
            print(f"[ERROR] Database connection failed: {e}")
            print(f"  Make sure MySQL is running and DATABASE_URL is correct")
            print(f"  Current DATABASE_URL: {Config.DATABASE_URL}")

if __name__ == '__main__':
    setup_database()

