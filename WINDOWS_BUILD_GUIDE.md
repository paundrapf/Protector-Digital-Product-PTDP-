# 🪟 Building Windows .exe Files

## Problem
Current builds are Linux ELF executables, not Windows .exe files.

## Solution Options

### Option 1: Build on Windows Machine ✅ RECOMMENDED
```bash
# On Windows with Python installed
pip install pyinstaller customtkinter cryptography pycryptodome

# Build Viewer
pyinstaller build_viewer_modern.spec

# Build Creator  
pyinstaller build_creator.spec

# Results in dist/
# - PTDP-Viewer.exe
# - PTDP-Creator.exe
```

### Option 2: GitHub Actions (Cross-Platform CI/CD) 🚀 BEST
Create `.github/workflows/build.yml`:

```yaml
name: Build Executables

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    strategy:
      matrix:
        os: [windows-latest, ubuntu-latest, macos-latest]
    runs-on: ${{ matrix.os }}
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pyinstaller
    
    - name: Build Viewer
      run: pyinstaller build_viewer_modern.spec
    
    - name: Build Creator
      run: pyinstaller build_creator.spec
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: PTDP-${{ matrix.os }}
        path: dist/
```

**Benefits**:
- ✅ Automatic builds for Windows, Linux, macOS
- ✅ Runs on every commit
- ✅ Free for public repos
- ✅ Professional CI/CD

### Option 3: Wine + PyInstaller (Linux → Windows)
```bash
# Install Wine
sudo apt-get install wine wine64

# Install Python for Windows via Wine
wget https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe
wine python-3.12.1-amd64.exe

# Install PyInstaller in Wine
wine pip install pyinstaller customtkinter cryptography

# Build
wine pyinstaller build_viewer_modern.spec
```

**Note**: Complex, may have issues with dependencies.

### Option 4: Docker with Windows Base
```dockerfile
FROM mcr.microsoft.com/windows/servercore:ltsc2022

# Install Python
# Build with PyInstaller
```

**Note**: Requires Windows containers support.

## Current Status

### Available Now:
- ✅ **PTDP-Viewer-Linux** (32.3 MB)
- ✅ **PTDP-Creator-Linux** (31.4 MB)

### Coming Soon:
- ⏳ **PTDP-Viewer.exe** (Windows)
- ⏳ **PTDP-Creator.exe** (Windows)
- ⏳ **PTDP-Viewer-macOS** (macOS)
- ⏳ **PTDP-Creator-macOS** (macOS)

## Quick Fix for Website

Website updated to show:
```
Download for Linux
Linux executable • Free for end users
Windows & macOS versions coming soon!
```

## Instructions for Windows Build

### If you have Windows machine:

1. **Install Python 3.12**
   - Download from python.org
   - Check "Add to PATH"

2. **Install dependencies**
   ```cmd
   pip install -r requirements.txt
   pip install pyinstaller
   ```

3. **Build executables**
   ```cmd
   pyinstaller build_viewer_modern.spec
   pyinstaller build_creator.spec
   ```

4. **Copy to website**
   ```cmd
   copy dist\PTDP-Viewer.exe website\downloads\
   copy dist\PTDP-Creator.exe website\downloads\
   ```

5. **Update website HTML**
   - Add Windows download buttons
   - Update file sizes
   - Add `.exe` extension

## File Naming Convention

```
PTDP-Viewer-Linux      # Linux (no extension, ELF)
PTDP-Viewer.exe        # Windows
PTDP-Viewer-macOS      # macOS (no extension, Mach-O)

PTDP-Creator-Linux     # Linux
PTDP-Creator.exe       # Windows  
PTDP-Creator-macOS     # macOS
```

## Current Website Downloads

Updated download handler to support platform-specific files:

```javascript
// Downloads PTDP-Viewer-Linux instead of PTDP-Viewer
const platform = btn.dataset.platform || 'Linux';
const filename = `PTDP-${type}-${platform}`;
```

## Recommended Next Steps

1. **Set up GitHub Actions** (Option 2)
   - Automatic builds for all platforms
   - No manual work needed
   - Professional solution

2. **Or build manually on Windows**
   - Quick one-time setup
   - Get .exe files immediately

3. **Update website when .exe ready**
   - Add Windows download buttons
   - Show platform selector
   - Auto-detect user's OS

## Testing

After building .exe files:

```cmd
# Test on Windows
PTDP-Viewer.exe
PTDP-Creator.exe

# Check file size
dir dist\PTDP-*.exe

# Test with sample files
```

---

**Current Status**: Linux builds ready ✅  
**Next**: Need Windows machine or GitHub Actions for .exe builds 🪟
