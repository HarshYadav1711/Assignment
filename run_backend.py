"""
Run script for the Flask backend.
Run this from the project root: python run_backend.py
"""
import sys
import os
from pathlib import Path

# Ensure we're in the project root
project_root = Path(__file__).parent
os.chdir(project_root)

# Add project root to Python path
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Now import and run the app
from backend.app import app

if __name__ == '__main__':
    print("=" * 50)
    print("AI Study Tool - Backend Server")
    print("=" * 50)
    print(f"Starting server on http://localhost:5000")
    print(f"Project root: {project_root}")
    print("=" * 50)
    app.run(debug=app.config.get('DEBUG', False), host='0.0.0.0', port=5000)

