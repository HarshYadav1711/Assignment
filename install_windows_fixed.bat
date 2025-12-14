@echo off
echo ========================================
echo AI Study Tool - Windows Installation (Fixed)
echo ========================================
echo.
echo This script installs packages using pre-built wheels
echo to avoid compilation errors on Windows.
echo.

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
echo Step 3: Installing numpy (pre-built wheel - avoids GCC issues)...
pip install "numpy>=1.24.3,<1.27.0" --only-binary :all:
if errorlevel 1 (
    echo WARNING: NumPy pre-built wheel failed
    echo Trying specific version...
    pip install numpy==1.26.4 --only-binary :all:
    if errorlevel 1 (
        echo Trying older version...
        pip install numpy==1.24.3 --only-binary :all:
        if errorlevel 1 (
            echo ERROR: Failed to install numpy with pre-built wheels
            echo You may need to use conda: conda install numpy
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
echo Step 5: Installing remaining dependencies...
pip install flask==3.0.0 flask-cors==4.0.0 flask-sqlalchemy==3.1.1
pip install pymysql==1.1.0 cryptography==41.0.7
pip install openai==1.3.0 google-generativeai==0.3.0
pip install youtube-transcript-api==0.6.1
pip install PyPDF2==3.0.1 pypdf==3.17.0
pip install python-dotenv==1.0.0 requests==2.31.0
pip install gunicorn==21.2.0 moviepy==1.0.3 pydub==0.25.1

echo.
echo ========================================
echo Installation complete!
echo ========================================
echo.
echo Verify installation:
python -c "import numpy, PIL, faiss; print('Core packages installed successfully!')"
if errorlevel 1 (
    echo WARNING: Some packages may not be installed correctly
    echo Check error messages above
)
echo.
pause

