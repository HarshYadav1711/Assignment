# AI Study Tool - Windows PowerShell Installation Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "AI Study Tool - Windows Installation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
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
pip install "numpy>=1.24.3,<1.27.0" --only-binary :all:
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: Pre-built wheel failed, trying regular install..." -ForegroundColor Yellow
    pip install "numpy>=1.24.3,<1.27.0"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install numpy" -ForegroundColor Red
        Write-Host "Try: pip install numpy==1.26.4 --only-binary :all:" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
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

