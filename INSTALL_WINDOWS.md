# Windows Installation Guide

## Common Installation Issues on Windows

### Issue 1: Pillow Build Error

If you encounter `KeyError: '__version__'` or `Failed to build 'Pillow'`, try these solutions:

#### Solution 1: Install Pre-built Pillow (Recommended)
```bash
pip install --upgrade pip setuptools wheel
pip install Pillow
```

#### Solution 2: Install Build Tools
If Solution 1 doesn't work, you may need Visual C++ Build Tools:
1. Download and install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. During installation, select "C++ build tools"
3. Restart your terminal and try again

#### Solution 3: Use Conda (Alternative)
```bash
conda install pillow
pip install -r requirements.txt
```

### Issue 2: FAISS Installation

If `faiss-cpu` fails to install:

```bash
# Try installing without version constraint first
pip install faiss-cpu

# If that fails, try:
pip install --upgrade pip
pip install faiss-cpu --no-cache-dir
```

### Issue 3: MoviePy Dependencies

MoviePy might need `ffmpeg` on Windows:

1. Download ffmpeg from: https://ffmpeg.org/download.html
2. Extract and add to PATH, or
3. Install via conda: `conda install ffmpeg`

### Complete Installation Steps for Windows

```bash
# 1. Upgrade pip and build tools
python -m pip install --upgrade pip setuptools wheel

# 2. Install Pillow first (separately)
pip install Pillow

# 3. Install other dependencies
pip install -r requirements.txt

# If step 3 fails, install packages individually:
pip install flask flask-cors flask-sqlalchemy
pip install pymysql cryptography
pip install openai google-generativeai
pip install youtube-transcript-api
pip install PyPDF2 pypdf
pip install faiss-cpu
pip install numpy python-dotenv requests
pip install gunicorn moviepy pydub
```

### Alternative: Use Pre-built Wheels

If you continue having build issues, you can use pre-built wheels:

```bash
pip install --only-binary :all: -r requirements.txt
```

Note: This will only install packages that have pre-built wheels available.

### Troubleshooting

1. **Clear pip cache**:
   ```bash
   pip cache purge
   ```

2. **Use virtual environment** (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Check Python version**:
   ```bash
   python --version
   ```
   Ensure you're using Python 3.9 or higher.

4. **Install Visual C++ Redistributable**:
   Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe

