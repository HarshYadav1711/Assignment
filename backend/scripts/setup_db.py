"""
Database setup script.
Creates tables and optionally seeds initial data.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app import app, db
from backend.config import Config

def setup_database():
    """Create database tables"""
    with app.app_context():
        db.create_all()
        print("✓ Database tables created successfully")
        
        # Test connection
        try:
            db.session.execute(db.text("SELECT 1"))
            print("✓ Database connection successful")
        except Exception as e:
            print(f"✗ Database connection failed: {e}")
            print(f"  Make sure MySQL is running and DATABASE_URL is correct")
            print(f"  Current DATABASE_URL: {Config.DATABASE_URL}")

if __name__ == '__main__':
    setup_database()

