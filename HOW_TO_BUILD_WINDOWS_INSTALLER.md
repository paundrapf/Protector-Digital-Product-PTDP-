# 🪟 How to Build Windows .EXE Installer

## ⚠️ IMPORTANT

**Files di screenshot Anda (PTDP-Viewer, PTDP-Creator) adalah Linux ELF binaries, BUKAN Windows .exe!**

Untuk mendapatkan **real Windows .exe installer**, Anda **HARUS** build di **Windows machine**.

## 🎯 Yang Sudah Disiapkan

Semua files untuk build Windows installer sudah ready:

```
✅ installer_windows.iss          - Inno Setup script
✅ build_windows_installer.py     - Automated build script  
✅ build_windows.spec              - PyInstaller config
✅ WINDOWS_INSTALLER_GUIDE.md      - Complete guide (200+ lines)
✅ website/                        - Updated dengan installer download
```

## 🚀 Quick Start (Windows Only!)

### Prerequisites

1. **Windows 10 atau 11 (64-bit)**
2. **Python 3.8+** - https://www.python.org/downloads/
3. **Git** - https://git-scm.com/downloads
4. **Inno Setup 6.x** - https://jrsoftware.org/isdl.php

### Installation

```powershell
# 1. Clone repository
git clone https://github.com/paundrapf/Protector-Digital-Product-PTDP-.git
cd Protector-Digital-Product-PTDP-

# 2. Install Python dependencies
pip install -r requirements.txt
pip install pyinstaller

# 3. Install Inno Setup
# Download dari https://jrsoftware.org/isdl.php
# Install ke: C:\Program Files (x86)\Inno Setup 6\
```

### Build Installer

**Method 1: Automatic (Recommended)**

```powershell
python build_windows_installer.py
```

Script ini akan:
- ✓ Check semua dependencies
- ✓ Build PTDP-Creator.exe dan PTDP-Viewer.exe
- ✓ Create installer dengan Inno Setup
- ✓ Copy ke website/downloads/

**Method 2: Manual**

```powershell
# Build executables
pyinstaller --clean --noconfirm build_windows.spec

# Create installer
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer_windows.iss

# Copy to website
copy installer_output\PTDP-Setup-v2.0.exe website\downloads\PTDP-Setup-Windows.exe
```

## 📦 Output

Setelah build selesai:

```
installer_output/
  └── PTDP-Setup-v2.0.exe         # Windows installer (~35 MB)

dist/windows/
  ├── PTDP-Creator.exe             # Standalone Creator (~32 MB)
  └── PTDP-Viewer.exe              # Standalone Viewer (~33 MB)

website/downloads/
  └── PTDP-Setup-Windows.exe       # Ready untuk download
```

## 🧪 Testing

```powershell
# Test installer
.\installer_output\PTDP-Setup-v2.0.exe

# Verify installation
"C:\Program Files\PTDP\PTDP-Creator.exe"
"C:\Program Files\PTDP\PTDP-Viewer.exe"
```

## 📋 Checklist

Before release:

- [ ] Build completed tanpa errors
- [ ] Installer tested di clean Windows 10/11
- [ ] Both apps installed successfully
- [ ] Start Menu shortcuts created
- [ ] Desktop icons working
- [ ] Apps run without errors
- [ ] Uninstaller works properly
- [ ] File uploaded ke website/downloads/

## 🌐 Update Website

Installer sudah integrated ke website! Just upload file:

```powershell
# Upload PTDP-Setup-Windows.exe ke folder website/downloads/
# Website akan automatically show download button
```

## 🐛 Troubleshooting

### Error: "This app can't run on your PC"
**Fix:** Anda mencoba run Linux binary di Windows. Build di Windows!

### Error: "PyInstaller not found"
```powershell
pip install pyinstaller
```

### Error: "Inno Setup not found"
**Fix:** Install Inno Setup dari https://jrsoftware.org/isdl.php

### Warning: "Windows protected your PC"
**Fix:** Click "More info" → "Run anyway"
Atau sign executable dengan code signing certificate.

## 💡 Alternative Options

Jika tidak punya Windows machine:

### Option 1: GitHub Actions (Recommended)
- Push code ke GitHub
- Workflow akan auto-build untuk Windows/Linux/macOS
- Download artifacts dari Actions tab

### Option 2: Windows VM
- VirtualBox: https://www.virtualbox.org/
- VMware: https://www.vmware.com/
- Hyper-V (built-in Windows Pro)

### Option 3: Cloud Windows
- Azure: https://azure.microsoft.com/
- AWS EC2: https://aws.amazon.com/ec2/
- DigitalOcean: https://www.digitalocean.com/

## 📚 Documentation

- **Complete Guide:** `WINDOWS_INSTALLER_GUIDE.md` (200+ lines)
- **Build Summary:** `BUILD_SUMMARY.md`
- **Build Options:** `WINDOWS_BUILD_GUIDE.md`

## 🎓 What You Get

### Windows Installer Includes:
- ✅ PTDP Creator.exe
- ✅ PTDP Viewer.exe
- ✅ Documentation (README, USER_GUIDE, QUICKSTART)
- ✅ Start Menu shortcuts
- ✅ Desktop icons (optional)
- ✅ Uninstaller
- ✅ Registry entries

### Installation Process:
1. User double-clicks `PTDP-Setup-v2.0.exe`
2. Setup wizard appears
3. User chooses install location
4. User selects options (desktop icons, etc.)
5. Installation completes
6. Shortcuts created
7. Apps ready to use!

## 🔒 Security

Installer akan:
- ✓ Check 64-bit Windows
- ✓ Request admin privileges
- ✓ Verify installation path
- ✓ Create proper registry entries
- ✓ Allow clean uninstall

## 📊 File Sizes

Expected sizes:
- `PTDP-Creator.exe`: ~32 MB
- `PTDP-Viewer.exe`: ~33 MB
- `PTDP-Setup-v2.0.exe`: ~35-40 MB (includes both + installer)

## 🎯 Next Steps

1. **Get Windows machine** (physical, VM, or cloud)
2. **Follow Quick Start** steps above
3. **Build installer** dengan `python build_windows_installer.py`
4. **Test thoroughly** di clean Windows
5. **Upload** to website/downloads/
6. **Announce** release!

---

**Need Help?** Read `WINDOWS_INSTALLER_GUIDE.md` untuk detailed instructions.

**Have Questions?** Open an issue di GitHub.
