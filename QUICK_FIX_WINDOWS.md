# Quick Fix for Windows Installation Issues

## 🚀 Fastest Solution (Recommended)

Run this in PowerShell or Command Prompt:

```powershell
# Step 1: Upgrade pip and build tools
python -m pip install --upgrade pip setuptools wheel

# Step 2: Install Pillow with pre-built wheel (avoids build errors)
pip install Pillow --only-binary :all:

# Step 3: Install numpy with pre-built wheel (avoids GCC compilation)
# IMPORTANT: Use --only-binary to avoid "NumPy requires GCC >= 8.4" error
pip install numpy --only-binary :all:
# If that fails, try: pip install numpy==1.26.4 --only-binary :all:
# Or: pip install numpy==1.24.3 --only-binary :all:

# Step 4: Install faiss-cpu
pip install faiss-cpu

# Step 5: Install everything else
pip install -r requirements.txt
```

## 🔧 Alternative: Use Installation Scripts

### Option 1: Batch Script (Command Prompt)
```cmd
install_windows.bat
```

### Option 2: PowerShell Script
```powershell
.\install_windows.ps1
```

## ⚠️ If NumPy Installation Fails

### Error: "NumPy requires GCC >= 8.4"

This means NumPy is trying to build from source. Use pre-built wheels instead:

```bash
# Try specific version with pre-built wheel
pip install numpy==1.26.4 --only-binary :all:

# Or try latest compatible version
pip install numpy --only-binary :all:
```

### If Pre-built Wheels Don't Work

1. **Upgrade pip and setuptools**:
   ```bash
   python -m pip install --upgrade pip setuptools wheel
   ```

2. **Try older NumPy version**:
   ```bash
   pip install numpy==1.24.3 --only-binary :all:
   ```

3. **Use conda instead** (most reliable):
   ```bash
   conda install numpy
   ```

## ⚠️ If Pillow Still Fails

### Install Visual C++ Build Tools

1. Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Run installer
3. Select "C++ build tools" workload
4. Install and restart terminal
5. Try installation again

### Or Use Conda (Easiest Alternative)

```bash
# Install Miniconda from: https://docs.conda.io/en/latest/miniconda.html

# Then:
conda create -n study_tool python=3.10
conda activate study_tool
conda install pillow numpy
pip install -r requirements.txt
```

## 📝 Manual Installation (If All Else Fails)

Install packages one by one to identify the problematic one:

```bash
pip install flask flask-cors flask-sqlalchemy
pip install pymysql cryptography
pip install openai google-generativeai
pip install youtube-transcript-api
pip install PyPDF2 pypdf
pip install faiss-cpu
pip install python-dotenv requests
pip install gunicorn moviepy pydub
```

## ✅ Verify Installation

```bash
python -c "import flask, openai, faiss, PIL; print('All packages installed successfully!')"
```

If this runs without errors, you're good to go!

