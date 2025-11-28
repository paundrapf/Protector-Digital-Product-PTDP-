#!/usr/bin/env python3
"""
PTDP Portable Windows Build Script
Creates standalone .exe files that work WITHOUT installation

USER FRIENDLY APPROACH:
- Download .exe
- Double-click to run
- NO installation needed!
- NO setup wizard!
- Just works!
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_step(msg):
    print(f"{Colors.OKBLUE}▶ {msg}{Colors.ENDC}")

def print_success(msg):
    print(f"{Colors.OKGREEN}✓ {msg}{Colors.ENDC}")

def print_error(msg):
    print(f"{Colors.FAIL}✗ {msg}{Colors.ENDC}")

def main():
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║                                                           ║")
    print("║          PTDP Portable Windows Builder                   ║")
    print("║          Download → Double-Click → Use!                   ║")
    print("║                                                           ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}\n")
    
    # Check Windows
    if sys.platform != 'win32':
        print_error("Must run on Windows!")
        print("\n💡 Options:")
        print("  1. Use Windows machine")
        print("  2. Use GitHub Actions (automatic)")
        print("  3. Use Windows VM")
        sys.exit(1)
    
    print_success("Running on Windows")
    
    # Check PyInstaller
    try:
        import PyInstaller
        print_success(f"PyInstaller {PyInstaller.__version__}")
    except ImportError:
        print_error("PyInstaller not found!")
        print("Install: pip install pyinstaller")
        sys.exit(1)
    
    # Clean previous builds
    print_step("Cleaning previous builds...")
    for dir_path in ['build', 'dist']:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
    print_success("Cleaned")
    
    # Build portable executables
    print_step("Building portable executables...")
    print("  This creates standalone .exe files")
    print("  No installation needed - just run!\n")
    
    result = subprocess.run([
        'pyinstaller',
        '--clean',
        '--noconfirm',
        'build_portable_windows.spec'
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print_error("Build failed!")
        print(result.stderr)
        sys.exit(1)
    
    print_success("Build completed!")
    
    # Check output
    viewer_exe = Path('dist/PTDP-Viewer.exe')
    creator_exe = Path('dist/PTDP-Creator.exe')
    
    if not viewer_exe.exists() or not creator_exe.exists():
        print_error("Executables not found!")
        sys.exit(1)
    
    viewer_size = viewer_exe.stat().st_size / (1024 * 1024)
    creator_size = creator_exe.stat().st_size / (1024 * 1024)
    
    print(f"\n{Colors.OKGREEN}📦 Output Files:{Colors.ENDC}")
    print(f"   PTDP-Viewer.exe:  {viewer_size:.1f} MB")
    print(f"   PTDP-Creator.exe: {creator_size:.1f} MB")
    
    # Copy to website downloads
    print_step("Copying to website downloads...")
    downloads_dir = Path('website/downloads')
    downloads_dir.mkdir(parents=True, exist_ok=True)
    
    shutil.copy2(viewer_exe, downloads_dir / 'PTDP-Viewer.exe')
    shutil.copy2(creator_exe, downloads_dir / 'PTDP-Creator.exe')
    print_success("Copied to website/downloads/")
    
    # Create README for users
    readme_content = """# PTDP - How to Use

## Super Simple! 🚀

### For End Users (Read PDFs):
1. Download PTDP-Viewer.exe
2. Double-click to run
3. Open .ptdp file
4. Enter license key
5. Read your PDF!

### For Sellers (Protect PDFs):
1. Download PTDP-Creator.exe
2. Double-click to run
3. Select your PDF
4. Protect it!
5. Generate license keys
6. Sell to customers!

## NO Installation Needed!

These are portable executables. Just download and run.
No setup wizard. No admin rights. Just works!

## First Time Running

Windows may show "Windows protected your PC" warning.
This is normal for new software.

How to run:
1. Click "More info"
2. Click "Run anyway"

Your files are safe! This is open source software.

## Need Help?

- Read USER_GUIDE.md
- Check QUICKSTART.md
- Visit our website
"""
    
    with open(downloads_dir / 'README.txt', 'w') as f:
        f.write(readme_content)
    
    print_success("Created README.txt for users")
    
    print(f"\n{Colors.OKGREEN}{Colors.BOLD}")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║                                                           ║")
    print("║                 BUILD SUCCESSFUL! ✓                       ║")
    print("║                                                           ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")
    
    print("\n📍 Files ready in: website/downloads/")
    print("\n🎯 User Experience:")
    print("   1. User downloads .exe")
    print("   2. Double-clicks to run")
    print("   3. App opens - ready to use!")
    print("   4. NO installation required!")
    
    print("\n💡 Next Steps:")
    print("   1. Test both .exe files")
    print("   2. Verify they run without installation")
    print("   3. Check file sizes on website")
    print("   4. Deploy to production!")

if __name__ == '__main__':
    main()
