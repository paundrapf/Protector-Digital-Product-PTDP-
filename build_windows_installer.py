#!/usr/bin/env python3
"""
PTDP Windows Installer Builder
Builds Windows .exe files and creates installer using PyInstaller + Inno Setup
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Colors for output
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
    print(f"{Colors.OKBLUE}► {msg}{Colors.ENDC}")

def print_success(msg):
    print(f"{Colors.OKGREEN}✓ {msg}{Colors.ENDC}")

def print_error(msg):
    print(f"{Colors.FAIL}✗ {msg}{Colors.ENDC}")

def print_warning(msg):
    print(f"{Colors.WARNING}⚠ {msg}{Colors.ENDC}")

def check_platform():
    """Check if running on Windows"""
    if sys.platform != 'win32':
        print_error("This script must be run on Windows!")
        print_warning("Current platform: " + sys.platform)
        print("\nOptions:")
        print("1. Run this on a Windows machine")
        print("2. Use GitHub Actions (see .github/workflows/build.yml)")
        print("3. Use a Windows VM or dual boot")
        sys.exit(1)
    print_success("Running on Windows")

def check_dependencies():
    """Check if required tools are installed"""
    print_step("Checking dependencies...")
    
    # Check Python
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print_success(f"Python {python_version}")
    
    # Check PyInstaller
    try:
        import PyInstaller
        print_success(f"PyInstaller {PyInstaller.__version__}")
    except ImportError:
        print_error("PyInstaller not found!")
        print("Install with: pip install pyinstaller")
        sys.exit(1)
    
    # Check Inno Setup
    iscc_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
    ]
    
    iscc_path = None
    for path in iscc_paths:
        if os.path.exists(path):
            iscc_path = path
            break
    
    if not iscc_path:
        print_warning("Inno Setup not found!")
        print("Download from: https://jrsoftware.org/isdl.php")
        print("Installer will not be created, but .exe files will be built.")
        return None
    
    print_success(f"Inno Setup found at {iscc_path}")
    return iscc_path

def clean_build():
    """Clean previous build artifacts"""
    print_step("Cleaning previous builds...")
    
    dirs_to_clean = ['build', 'dist/windows', 'installer_output']
    for dir_path in dirs_to_clean:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            print(f"  Removed {dir_path}")
    
    print_success("Cleaned build directories")

def build_executables():
    """Build Windows executables using PyInstaller"""
    print_step("Building Windows executables...")
    
    # Build Creator
    print("  Building PTDP Creator...")
    result = subprocess.run([
        'pyinstaller',
        '--clean',
        '--noconfirm',
        'build_windows.spec'
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print_error("Failed to build Creator!")
        print(result.stderr)
        sys.exit(1)
    
    print_success("Built PTDP Creator")
    
    # Check if files exist
    creator_path = Path('dist/windows/PTDP-Creator.exe')
    viewer_path = Path('dist/windows/PTDP-Viewer.exe')
    
    if creator_path.exists():
        size = creator_path.stat().st_size / (1024 * 1024)
        print(f"    Creator: {size:.1f} MB")
    else:
        print_error("Creator.exe not found!")
        sys.exit(1)
    
    if viewer_path.exists():
        size = viewer_path.stat().st_size / (1024 * 1024)
        print(f"    Viewer: {size:.1f} MB")
    else:
        print_error("Viewer.exe not found!")
        sys.exit(1)

def create_installer(iscc_path):
    """Create installer using Inno Setup"""
    if not iscc_path:
        print_warning("Skipping installer creation (Inno Setup not found)")
        return
    
    print_step("Creating Windows installer...")
    
    result = subprocess.run([
        iscc_path,
        'installer_windows.iss'
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print_error("Failed to create installer!")
        print(result.stderr)
        sys.exit(1)
    
    # Check installer output
    installer_path = Path('installer_output/PTDP-Setup-v2.0.exe')
    if installer_path.exists():
        size = installer_path.stat().st_size / (1024 * 1024)
        print_success(f"Installer created: {size:.1f} MB")
        print(f"    Location: {installer_path.absolute()}")
    else:
        print_error("Installer not found!")

def copy_to_website():
    """Copy installer to website downloads"""
    print_step("Copying to website downloads...")
    
    # Create downloads directory
    downloads_dir = Path('website/downloads')
    downloads_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy installer
    installer_src = Path('installer_output/PTDP-Setup-v2.0.exe')
    if installer_src.exists():
        installer_dst = downloads_dir / 'PTDP-Setup-Windows.exe'
        shutil.copy2(installer_src, installer_dst)
        size = installer_dst.stat().st_size / (1024 * 1024)
        print_success(f"Copied installer to website ({size:.1f} MB)")
    
    # Also copy standalone executables
    for exe_name in ['PTDP-Creator.exe', 'PTDP-Viewer.exe']:
        src = Path(f'dist/windows/{exe_name}')
        if src.exists():
            dst = downloads_dir / exe_name
            shutil.copy2(src, dst)
            print(f"  Copied {exe_name}")

def main():
    """Main build process"""
    print(f"{Colors.HEADER}")
    print("═" * 60)
    print("  PTDP Windows Installer Builder")
    print("═" * 60)
    print(f"{Colors.ENDC}\n")
    
    check_platform()
    iscc_path = check_dependencies()
    clean_build()
    build_executables()
    create_installer(iscc_path)
    copy_to_website()
    
    print(f"\n{Colors.OKGREEN}{Colors.BOLD}")
    print("═" * 60)
    print("  BUILD COMPLETED SUCCESSFULLY!")
    print("═" * 60)
    print(f"{Colors.ENDC}")
    
    print("\nOutput files:")
    print("  • Executables: dist/windows/")
    print("  • Installer: installer_output/PTDP-Setup-v2.0.exe")
    print("  • Website: website/downloads/")
    
    print("\nNext steps:")
    print("  1. Test the installer on a clean Windows machine")
    print("  2. Update website to offer installer download")
    print("  3. Create release on GitHub")

if __name__ == '__main__':
    main()
