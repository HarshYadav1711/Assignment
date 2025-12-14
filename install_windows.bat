@echo off
echo ========================================
echo AI Study Tool - Windows Installation
echo ========================================
echo.

REM Change to script directory
cd /d "%~dp0"
echo Working directory: %CD%
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
    echo WARNING: Pillow installation with pre-built wheel failed
    echo Trying regular installation...
    pip install Pillow
    if errorlevel 1 (
        echo ERROR: Failed to install Pillow
        echo Please install Visual C++ Build Tools and try again
        pause
        exit /b 1
    )
)

echo.
echo Step 3: Installing numpy (required for faiss)...
echo Using pre-built wheel to avoid GCC compilation issues...
echo Trying latest NumPy with pre-built wheel...
pip install numpy --only-binary :all:
if errorlevel 1 (
    echo WARNING: Latest NumPy failed, trying NumPy 2.0...
    pip install "numpy>=2.0.0" --only-binary :all:
    if errorlevel 1 (
        echo WARNING: NumPy 2.0 failed, trying NumPy 1.26.4...
        pip install numpy==1.26.4 --only-binary :all:
        if errorlevel 1 (
            echo ERROR: All pre-built wheel attempts failed
            echo Your Python version may not have pre-built wheels
            echo Try using conda: conda install numpy
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
    echo This might be due to missing dependencies
    echo Try: pip install --upgrade pip
    echo Then: pip install faiss-cpu --no-cache-dir
)

echo.
echo Step 5: Installing remaining dependencies...
if not exist "requirements.txt" (
    echo ERROR: requirements.txt not found in current directory
    echo Current directory: %CD%
    echo Please run this script from the project root directory
    pause
    exit /b 1
)
pip install -r requirements.txt
if errorlevel 1 (
    echo WARNING: Some packages failed to install
    echo Check the error messages above
    echo You may need to install packages individually
)

echo.
echo ========================================
echo Installation complete!
echo ========================================
echo.
echo If you encountered errors, see INSTALL_WINDOWS.md for troubleshooting
pause

