@echo off
REM Complete installation script that handles directory and all dependencies
echo ========================================
echo AI Study Tool - Complete Installation
echo ========================================
echo.

REM Change to script directory (where this .bat file is located)
cd /d "%~dp0"
echo Working directory: %CD%
echo.

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo ERROR: requirements.txt not found!
    echo.
    echo Please ensure you're running this script from the project root.
    echo The script should be in the same folder as requirements.txt
    echo.
    echo Current directory: %CD%
    echo.
    pause
    exit /b 1
)

echo Step 1: Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo ERROR: Failed to upgrade pip
    pause
    exit /b 1
)

echo.
echo Step 2: Installing Pillow (pre-built wheel)...
pip install Pillow --only-binary :all:
if errorlevel 1 (
    echo WARNING: Pillow pre-built wheel failed
    echo Trying regular installation...
    pip install Pillow
    if errorlevel 1 (
        echo ERROR: Failed to install Pillow
        echo Please install Visual C++ Build Tools
        pause
        exit /b 1
    )
)

echo.
echo Step 3: Installing numpy (pre-built wheel)...
echo Note: Python 3.13 may only have NumPy 2.x wheels available
echo Trying latest NumPy...
pip install numpy --only-binary :all:
if errorlevel 1 (
    echo WARNING: Latest NumPy failed, trying NumPy 2.x...
    pip install "numpy>=2.0.0" --only-binary :all:
    if errorlevel 1 (
        echo WARNING: NumPy 2.x failed, trying NumPy 1.26.4...
        pip install numpy==1.26.4 --only-binary :all:
        if errorlevel 1 (
            echo ERROR: All pre-built wheel attempts failed
            echo Your Python 3.13 may not have pre-built wheels for NumPy 1.x
            echo Solution: Use conda or downgrade to Python 3.11
            pause
            exit /b 1
        )
    )
)

echo.
echo Step 4: Installing faiss-cpu...
pip install faiss-cpu
if errorlevel 1 (
    echo WARNING: faiss-cpu installation failed
    echo This might work after numpy is installed
    echo Try: pip install faiss-cpu --no-cache-dir
)

echo.
echo Step 5: Installing remaining dependencies from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo WARNING: Some packages failed to install
    echo Check error messages above
    echo.
    echo You can try installing packages individually:
    echo pip install flask flask-cors flask-sqlalchemy
    echo pip install pymysql cryptography
    echo pip install openai google-generativeai
    echo pip install youtube-transcript-api
    echo pip install PyPDF2 pypdf
    echo pip install python-dotenv requests
    echo pip install gunicorn moviepy pydub
)

echo.
echo ========================================
echo Installation complete!
echo ========================================
echo.
echo Verifying installation...
python -c "import numpy, PIL, faiss; print('Core packages installed successfully!')" 2>nul
if errorlevel 1 (
    echo WARNING: Some packages may not be installed correctly
    echo Check error messages above
) else (
    echo.
    echo All core packages are working!
)
echo.
pause

