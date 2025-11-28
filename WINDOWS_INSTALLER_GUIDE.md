# 🪟 PTDP Windows Installer Guide

Complete guide untuk membuat **Windows .exe installer** yang profesional untuk PTDP.

## 📋 Overview

Installer ini akan membuat **setup wizard** yang proper untuk Windows, dengan fitur:
- ✅ Professional setup wizard (Inno Setup)
- ✅ Start Menu shortcuts
- ✅ Desktop icons (optional)
- ✅ Uninstaller
- ✅ 64-bit Windows support
- ✅ Admin privileges check
- ✅ File associations
- ✅ Proper directory structure

## 🛠️ Prerequisites

### 1. Windows Machine
Anda **HARUS** menggunakan Windows untuk build installer. Linux/macOS tidak bisa membuat Windows .exe yang proper.

### 2. Install Python 3.8+
```powershell
# Download dari python.org atau gunakan winget
winget install Python.Python.3.12
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
pip install pyinstaller
```

### 4. Install Inno Setup
Download dan install dari: https://jrsoftware.org/isdl.php

**Recommended version:** Inno Setup 6.x

Install ke lokasi default: `C:\Program Files (x86)\Inno Setup 6\`

## 🚀 Build Process

### Method 1: Automatic Build (Recommended)

Jalankan script otomatis:

```powershell
python build_windows_installer.py
```

Script ini akan:
1. ✓ Check dependencies
2. ✓ Clean previous builds
3. ✓ Build PTDP-Creator.exe
4. ✓ Build PTDP-Viewer.exe
5. ✓ Create installer (PTDP-Setup-v2.0.exe)
6. ✓ Copy ke website/downloads/

### Method 2: Manual Build

#### Step 1: Build Executables
```powershell
# Build using PyInstaller
pyinstaller --clean --noconfirm build_windows.spec
```

Output: `dist/windows/PTDP-Creator.exe` dan `dist/windows/PTDP-Viewer.exe`

#### Step 2: Create Installer
```powershell
# Using Inno Setup compiler
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer_windows.iss
```

Output: `installer_output/PTDP-Setup-v2.0.exe`

#### Step 3: Copy to Website
```powershell
# Copy installer
copy installer_output\PTDP-Setup-v2.0.exe website\downloads\PTDP-Setup-Windows.exe

# Copy standalone executables
copy dist\windows\PTDP-Creator.exe website\downloads\
copy dist\windows\PTDP-Viewer.exe website\downloads\
```

## 📦 Output Files

Setelah build berhasil, Anda akan mendapatkan:

```
installer_output/
  └── PTDP-Setup-v2.0.exe         # Full installer (~35-40 MB)

dist/windows/
  ├── PTDP-Creator.exe             # Standalone Creator (~32 MB)
  └── PTDP-Viewer.exe              # Standalone Viewer (~33 MB)

website/downloads/
  ├── PTDP-Setup-Windows.exe       # Installer untuk website
  ├── PTDP-Creator.exe             # Optional: standalone
  └── PTDP-Viewer.exe              # Optional: standalone
```

## 🧪 Testing

### 1. Test di Clean Windows Machine
Ideal untuk test di VM atau clean Windows install:
- Windows 10 64-bit
- Windows 11 64-bit

### 2. Run Installer
```powershell
# Double-click atau run:
.\PTDP-Setup-v2.0.exe
```

### 3. Verify Installation
Check locations:
- `C:\Program Files\PTDP\` - Installation directory
- Start Menu → PTDP - Shortcuts
- Desktop - Icons (if selected)

### 4. Test Applications
```powershell
# Run Creator
"C:\Program Files\PTDP\PTDP-Creator.exe"

# Run Viewer
"C:\Program Files\PTDP\PTDP-Viewer.exe"
```

### 5. Test Uninstaller
- Control Panel → Programs and Features → PTDP
- atau Start Menu → PTDP → Uninstall

## 🎯 Installer Features

### What Gets Installed

1. **Applications**
   - PTDP-Creator.exe
   - PTDP-Viewer.exe

2. **Documentation**
   - README.md
   - USER_GUIDE.md
   - QUICKSTART.md

3. **Shortcuts**
   - Start Menu → PTDP Creator
   - Start Menu → PTDP Viewer
   - Start Menu → User Guide
   - Desktop icons (optional)

4. **Registry Entries**
   - App registration
   - Uninstaller information

### Installation Options

User dapat memilih:
- ✓ Installation directory
- ✓ Create desktop icons
- ✓ Create quick launch icons
- ✓ Language (English/Indonesian)

## 🔧 Customization

### Edit Installer Script

File: `installer_windows.iss`

```pascal
; Change app info
#define MyAppName "PTDP - Protector Digital Product"
#define MyAppVersion "2.0"
#define MyAppPublisher "PTDP Team"

; Change install directory
DefaultDirName={autopf}\PTDP

; Add more files
Source: "path\to\file"; DestDir: "{app}"; Flags: ignoreversion
```

### Edit PyInstaller Config

File: `build_windows.spec`

```python
# Add more hidden imports
hiddenimports=[
    'your_module_here'
]

# Change exe name
exe = EXE(
    name='YourApp.exe',
    ...
)
```

## 🐛 Troubleshooting

### Problem: "This app can't run on your PC"
**Solution:** Anda mencoba run Linux binary di Windows. Harus build di Windows!

### Problem: PyInstaller fails
**Solutions:**
```powershell
# Update PyInstaller
pip install --upgrade pyinstaller

# Clear cache
rmdir /s /q build dist
pyinstaller --clean build_windows.spec
```

### Problem: Inno Setup not found
**Solutions:**
1. Install Inno Setup dari https://jrsoftware.org/isdl.php
2. Check path di `build_windows_installer.py`
3. Update path jika install di lokasi berbeda

### Problem: Missing DLL errors
**Solutions:**
```powershell
# Install Visual C++ Redistributable
# Download dari Microsoft
```

### Problem: "Windows protected your PC" warning
**Solutions:**
1. Click "More info" → "Run anyway"
2. Atau: Sign the .exe dengan code signing certificate

## 🌐 Update Website

Setelah build berhasil, update website untuk offer installer:

### 1. Edit HTML

```html
<!-- website/index.html -->
<div class="download-card">
    <h3>🪟 Windows Installer</h3>
    <p>Complete installer dengan setup wizard</p>
    <button onclick="downloadInstaller('Windows')">
        Download Installer (35 MB)
    </button>
    <div class="download-info">
        <span class="file-size">35 MB</span>
        <span class="platform">Windows 10/11 64-bit</span>
    </div>
</div>
```

### 2. Update JavaScript

```javascript
// website/script.js
function downloadInstaller(platform) {
    showNotification(`Downloading installer for ${platform}...`);
    
    const link = document.createElement('a');
    link.href = `downloads/PTDP-Setup-${platform}.exe`;
    link.download = `PTDP-Setup-${platform}.exe`;
    link.click();
    
    setTimeout(() => {
        showNotification(`✓ Download started!`, 'success');
    }, 500);
}
```

## 📚 Additional Resources

- **Inno Setup Documentation:** https://jrsoftware.org/ishelp/
- **PyInstaller Manual:** https://pyinstaller.org/en/stable/
- **Code Signing Guide:** https://docs.microsoft.com/en-us/windows/win32/seccrypto/cryptography-tools

## 🎓 Best Practices

1. **Always test on clean Windows VM** sebelum release
2. **Include version number** di filename
3. **Sign your executables** untuk avoid security warnings
4. **Provide checksums** (SHA256) untuk verify downloads
5. **Test uninstaller** pastikan clean uninstall
6. **Include README** dengan system requirements

## 📝 Checklist

Sebelum release, pastikan:

- [ ] Build berhasil tanpa errors
- [ ] Installer tested di Windows 10/11
- [ ] All shortcuts working
- [ ] Uninstaller working properly
- [ ] Documentation included
- [ ] Website updated dengan download link
- [ ] File sizes accurate di website
- [ ] SHA256 checksums generated
- [ ] Release notes prepared

## 🚀 Release Process

1. **Build installer** dengan `build_windows_installer.py`
2. **Test thoroughly** di Windows VM
3. **Generate checksums:**
   ```powershell
   certutil -hashfile PTDP-Setup-v2.0.exe SHA256
   ```
4. **Upload ke website** downloads folder
5. **Update website** dengan link dan info
6. **Create GitHub release** dengan installer attachment
7. **Announce** di documentation/README

---

**Need Help?** Check `WINDOWS_BUILD_GUIDE.md` atau GitHub Issues.
