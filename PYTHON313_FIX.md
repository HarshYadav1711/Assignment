# Python 3.13 Installation Fix

## Problem

You're using **Python 3.13**, which is very new. Many packages don't have pre-built wheels for NumPy 1.x on Python 3.13 yet. The available wheels are for NumPy 2.x.

## ✅ Solution Options

### Option 1: Install NumPy 2.x (Recommended)

NumPy 2.x works with Python 3.13 and has pre-built wheels:

```powershell
# Upgrade pip first
python -m pip install --upgrade pip setuptools wheel

# Install NumPy 2.x (has pre-built wheels for Python 3.13)
pip install "numpy>=2.0.0" --only-binary :all:

# Verify it works
python -c "import numpy; print(f'NumPy {numpy.__version__} installed!')"
```

**Note**: NumPy 2.x is compatible with faiss-cpu, so this should work fine.

### Option 2: Use Python 3.11 or 3.12 (Most Reliable)

Python 3.13 is very new. For best compatibility, use Python 3.11 or 3.12:

1. **Download Python 3.11 or 3.12**: https://www.python.org/downloads/
2. **Create new virtual environment**:
   ```powershell
   py -3.11 -m venv venv
   # Or
   py -3.12 -m venv venv
   ```
3. **Activate and install**:
   ```powershell
   venv\Scripts\activate
   pip install --upgrade pip
   pip install numpy --only-binary :all:
   pip install -r requirements.txt
   ```

### Option 3: Use Conda (Best for Scientific Packages)

Conda has pre-compiled packages that work with any Python version:

```bash
# Install Miniconda: https://docs.conda.io/en/latest/miniconda.html

# Create environment with Python 3.11 (most compatible)
conda create -n study_tool python=3.11
conda activate study_tool

# Install NumPy and Pillow via conda
conda install numpy pillow

# Install rest via pip
pip install -r requirements.txt
```

### Option 4: Install Without Version Constraint

Let pip find the best compatible version:

```powershell
# Remove version constraint and let pip decide
pip install numpy --only-binary :all: --upgrade

# This will install NumPy 2.x if that's what's available
```

## Why This Happens

- **Python 3.13** was released recently (October 2024)
- **NumPy 1.x** wheels for Python 3.13 may not exist yet
- **NumPy 2.x** has better Python 3.13 support
- **faiss-cpu** works with both NumPy 1.x and 2.x

## Recommended Approach

**For Python 3.13 users:**

1. Try NumPy 2.x first (it should work):
   ```powershell
   pip install "numpy>=2.0.0" --only-binary :all:
   ```

2. If that doesn't work, use Python 3.11 or 3.12 instead

3. Or use conda (most reliable)

## Verify Installation

After installing NumPy, verify everything works:

```powershell
python -c "import numpy; print(f'NumPy {numpy.__version__}')"
python -c "import faiss; print('faiss-cpu works!')"
python -c "import PIL; print('Pillow works!')"
```

## Updated Installation Command for Python 3.13

```powershell
# Complete installation for Python 3.13
python -m pip install --upgrade pip setuptools wheel

# Install NumPy 2.x (compatible with Python 3.13)
pip install "numpy>=2.0.0" --only-binary :all:

# Install Pillow
pip install Pillow --only-binary :all:

# Install faiss-cpu
pip install faiss-cpu

# Install rest
pip install -r requirements.txt
```

