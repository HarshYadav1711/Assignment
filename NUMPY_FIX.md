# NumPy Installation Fix for Windows

## Problem

You're seeing this error:
```
ERROR: NumPy requires GCC >= 8.4
```

This happens because:
- NumPy is trying to **build from source** (compile C code)
- Your system has **GCC 6.3.0** (too old)
- NumPy needs **GCC 8.4+** to compile

## ✅ Solution: Use Pre-built Wheels

Pre-built wheels are pre-compiled packages that don't need compilation. Use them!

### Quick Fix (Copy & Paste)

```powershell
# Upgrade pip first
python -m pip install --upgrade pip setuptools wheel

# Install NumPy with pre-built wheel (no compilation needed)
pip install numpy --only-binary :all:

# If that fails, try specific version
pip install numpy==1.26.4 --only-binary :all:

# Or try older version
pip install numpy==1.24.3 --only-binary :all:
```

### Step-by-Step Explanation

1. **`--only-binary :all:`** tells pip to ONLY use pre-built wheels
2. This skips compilation entirely
3. Works on Windows without needing GCC

### If Pre-built Wheels Don't Work

#### Option 1: Use Conda (Recommended)

Conda has pre-compiled NumPy that always works:

```bash
# Install Miniconda from: https://docs.conda.io/en/latest/miniconda.html

# Then:
conda create -n study_tool python=3.10
conda activate study_tool
conda install numpy
pip install -r requirements.txt
```

#### Option 2: Install Newer GCC

If you really need to compile:

1. Install **MSYS2**: https://www.msys2.org/
2. Update GCC to 8.4+:
   ```bash
   pacman -S mingw-w64-x86_64-gcc
   ```
3. Add to PATH and try again

#### Option 3: Use Older NumPy

Older versions might have pre-built wheels for your Python version:

```bash
pip install numpy==1.24.3 --only-binary :all:
```

### Verify Installation

```bash
python -c "import numpy; print(f'NumPy {numpy.__version__} installed successfully!')"
```

### Complete Installation Command

After fixing NumPy, install everything:

```powershell
# 1. Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# 2. Install NumPy with pre-built wheel
pip install numpy --only-binary :all:

# 3. Install Pillow with pre-built wheel
pip install Pillow --only-binary :all:

# 4. Install faiss-cpu
pip install faiss-cpu

# 5. Install rest of dependencies
pip install -r requirements.txt
```

## Why This Happens

- **Python 3.13** (newer) might not have pre-built wheels for all packages yet
- **NumPy 1.26.4+** requires newer GCC when building from source
- **Windows** doesn't come with GCC, so pip tries to use MinGW (old version)

## Best Practice

Always use pre-built wheels on Windows when possible:
```bash
pip install package_name --only-binary :all:
```

This is faster and avoids compilation issues!

