# AI Study Tool - Windows PowerShell Installation Script

# Change to script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "AI Study Tool - Windows Installation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Working directory: $PWD" -ForegroundColor Gray
Write-Host ""

# Step 1: Upgrade pip
Write-Host "Step 1: Upgrading pip, setuptools, and wheel..." -ForegroundColor Yellow
python -m pip install --upgrade pip setuptools wheel
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to upgrade pip" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Step 2: Install Pillow with pre-built wheel
Write-Host ""
Write-Host "Step 2: Installing Pillow (pre-built wheel)..." -ForegroundColor Yellow
pip install Pillow --only-binary :all:
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: Pillow pre-built wheel failed, trying regular install..." -ForegroundColor Yellow
    pip install Pillow
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install Pillow" -ForegroundColor Red
        Write-Host "Please install Visual C++ Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Step 3: Install numpy with pre-built wheel
Write-Host ""
Write-Host "Step 3: Installing numpy (using pre-built wheel)..." -ForegroundColor Yellow
Write-Host "Note: Python 3.13 may only have NumPy 2.x wheels available" -ForegroundColor Cyan
Write-Host "Trying latest NumPy..." -ForegroundColor Yellow
pip install numpy --only-binary :all:
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: Latest NumPy failed, trying NumPy 2.x..." -ForegroundColor Yellow
    pip install "numpy>=2.0.0" --only-binary :all:
    if ($LASTEXITCODE -ne 0) {
        Write-Host "WARNING: NumPy 2.x failed, trying NumPy 1.26.4..." -ForegroundColor Yellow
        pip install numpy==1.26.4 --only-binary :all:
        if ($LASTEXITCODE -ne 0) {
            Write-Host "ERROR: All pre-built wheel attempts failed" -ForegroundColor Red
            Write-Host "Your Python 3.13 may not have pre-built wheels for NumPy 1.x" -ForegroundColor Yellow
            Write-Host "Solution: Use conda or downgrade to Python 3.11" -ForegroundColor Yellow
            Write-Host "Try: conda install numpy" -ForegroundColor Yellow
            Write-Host "Or see PYTHON313_FIX.md for detailed instructions" -ForegroundColor Yellow
            Read-Host "Press Enter to exit"
            exit 1
        }
    }
}

# Step 4: Install faiss-cpu
Write-Host ""
Write-Host "Step 4: Installing faiss-cpu..." -ForegroundColor Yellow
pip install faiss-cpu
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: faiss-cpu installation failed" -ForegroundColor Yellow
    Write-Host "Try: pip install --upgrade pip" -ForegroundColor Yellow
    Write-Host "Then: pip install faiss-cpu --no-cache-dir" -ForegroundColor Yellow
}

# Step 5: Install remaining dependencies
Write-Host ""
Write-Host "Step 5: Installing remaining dependencies..." -ForegroundColor Yellow
if (-not (Test-Path "requirements.txt")) {
    Write-Host "ERROR: requirements.txt not found in current directory" -ForegroundColor Red
    Write-Host "Current directory: $PWD" -ForegroundColor Yellow
    Write-Host "Please run this script from the project root directory" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: Some packages failed to install" -ForegroundColor Yellow
    Write-Host "Check error messages above" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Installation complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "If you encountered errors, see INSTALL_WINDOWS.md for troubleshooting" -ForegroundColor Yellow
Read-Host "Press Enter to exit"

