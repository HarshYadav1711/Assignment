"""
Setup script for the AI Study Tool.
Helps initialize the project and check dependencies.
"""
import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is 3.9+"""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ is required")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}")
    return True

def check_node():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        print(f"✓ Node.js {result.stdout.strip()}")
        return True
    except FileNotFoundError:
        print("❌ Node.js is not installed")
        return False

def setup_backend():
    """Setup Python backend"""
    print("\n📦 Setting up backend...")
    
    # Create virtual environment
    if not os.path.exists('venv'):
        print("Creating virtual environment...")
        subprocess.run([sys.executable, '-m', 'venv', 'venv'])
    
    # Determine activation script
    if sys.platform == 'win32':
        pip = 'venv\\Scripts\\pip'
    else:
        pip = 'venv/bin/pip'
    
    # Install requirements
    print("Installing Python dependencies...")
    subprocess.run([pip, 'install', '-r', 'requirements.txt'])
    
    print("✓ Backend setup complete")

def setup_frontend():
    """Setup React frontend"""
    print("\n📦 Setting up frontend...")
    
    os.chdir('frontend')
    subprocess.run(['npm', 'install'])
    os.chdir('..')
    
    print("✓ Frontend setup complete")

def create_env_file():
    """Create .env file from example if it doesn't exist"""
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("✓ Created .env file from .env.example")
            print("⚠️  Please edit .env and add your API keys!")
        else:
            print("⚠️  .env.example not found, please create .env manually")

def main():
    print("🔥 AI Study Tool - Setup Script\n")
    
    if not check_python_version():
        sys.exit(1)
    
    check_node()
    
    create_env_file()
    
    setup_backend()
    setup_frontend()
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Edit .env file and add your API keys")
    print("2. Set up MySQL database")
    print("3. Run: python backend/scripts/setup_db.py")
    print("4. Start backend: cd backend && python app.py")
    print("5. Start frontend: cd frontend && npm start")

if __name__ == '__main__':
    main()

