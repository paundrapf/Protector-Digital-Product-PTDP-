# build.py
"""
Build script untuk compile PTPD tools menjadi executables
Requires: pip install pyinstaller
"""

import PyInstaller.__main__
import os
import sys
import shutil

def build_viewer():
    """Build PTPD Viewer untuk end-users"""
    print("\n" + "="*60)
    print("🔨 Building PTPD Viewer (End-User Application)")
    print("="*60)
    
    args = [
        'gui/viewer.py',
        '--name=PTPD-Viewer',
        '--onefile',
        '--windowed',
        '--clean',
        '--noconfirm',
        # Add hidden imports
        '--hidden-import=cryptography',
        '--hidden-import=cryptography.fernet',
        '--hidden-import=cryptography.hazmat',
        '--hidden-import=cryptography.hazmat.primitives',
        '--hidden-import=requests',
        '--hidden-import=psutil',
    ]
    
    # Add icon if exists
    if os.path.exists('assets/icon.ico'):
        args.append('--icon=assets/icon.ico')
    
    try:
        PyInstaller.__main__.run(args)
        print("\n✅ PTPD Viewer built successfully!")
        print(f"   Location: dist/PTPD-Viewer.exe")
    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        return False
    
    return True

def build_creator():
    """Build PTPD Creator untuk admin/sellers"""
    print("\n" + "="*60)
    print("🔨 Building PTPD Creator (Admin Tool)")
    print("="*60)
    
    args = [
        'gui/creator.py',
        '--name=PTPD-Creator',
        '--onefile',
        '--windowed',
        '--clean',
        '--noconfirm',
        '--hidden-import=cryptography',
        '--hidden-import=cryptography.fernet',
        '--hidden-import=cryptography.hazmat',
        '--hidden-import=cryptography.hazmat.primitives',
    ]
    
    if os.path.exists('assets/icon.ico'):
        args.append('--icon=assets/icon.ico')
    
    try:
        PyInstaller.__main__.run(args)
        print("\n✅ PTPD Creator built successfully!")
        print(f"   Location: dist/PTPD-Creator.exe")
    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        return False
    
    return True

def create_distribution_package():
    """Create distribution package dengan semua files yang dibutuhkan"""
    print("\n" + "="*60)
    print("📦 Creating Distribution Package")
    print("="*60)
    
    # Create dist folder structure
    dist_viewer = 'distribution/PTPD-Viewer'
    dist_creator = 'distribution/PTPD-Creator'
    
    os.makedirs(dist_viewer, exist_ok=True)
    os.makedirs(dist_creator, exist_ok=True)
    
    # Copy viewer
    if os.path.exists('dist/PTPD-Viewer.exe'):
        shutil.copy('dist/PTPD-Viewer.exe', dist_viewer)
        print("✅ Copied PTPD-Viewer.exe")
    
    # Copy creator
    if os.path.exists('dist/PTPD-Creator.exe'):
        shutil.copy('dist/PTPD-Creator.exe', dist_creator)
        print("✅ Copied PTPD-Creator.exe")
    
    # Create README for viewer
    viewer_readme = f"""
PTPD Viewer - User Guide
========================

WHAT IS THIS?
This application allows you to open protected .ptpd files.

HOW TO INSTALL:
1. Copy PTPD-Viewer.exe to any folder (e.g., C:\\Program Files\\PTPD Viewer)
2. Run PTPD-Viewer.exe
3. (Optional) Run register_ptpd.bat as Administrator to associate .ptpd files

HOW TO USE:
1. Open PTPD-Viewer.exe
2. Click "Open PTPD File" and select your .ptpd file
3. Enter your license key
4. Click "Unlock & View File"
5. The file will open in its default application

GETTING YOUR LICENSE KEY:
License keys are provided by the seller when you purchase a protected product.

SUPPORT:
For support, contact the product seller with:
- Your license key
- Your Device ID (shown at bottom of viewer)
- Error message (if any)

© 2024 PTPD Protection System
"""
    
    with open(f'{dist_viewer}/README.txt', 'w') as f:
        f.write(viewer_readme)
    print("✅ Created README.txt for viewer")
    
    # Create README for creator
    creator_readme = f"""
PTPD Creator - Admin Guide
===========================

WHAT IS THIS?
This tool allows you to protect your digital products with .ptpd format.

HOW TO USE:
1. Run PTPD-Creator.exe
2. Select file to protect
3. Fill in product details
4. Set protection options
5. Click "Create Protected File"
6. SAVE your master password!

GENERATING LICENSE KEYS:
After creating a protected file, you can generate license keys for buyers.

IMPORTANT:
- Keep your master password secret!
- Each product needs a unique Product ID
- Save all product IDs and passwords

For detailed documentation, see the main project README.

© 2024 PTPD Protection System
"""
    
    with open(f'{dist_creator}/README.txt', 'w') as f:
        f.write(creator_readme)
    print("✅ Created README.txt for creator")
    
    print(f"\n📦 Distribution packages created:")
    print(f"   {dist_viewer}/")
    print(f"   {dist_creator}/")

def main():
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "PTPD BUILD SYSTEM" + " "*25 + "║")
    print("╚" + "="*58 + "╝")
    
    # Check if pyinstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("\n❌ PyInstaller not found!")
        print("   Install it with: pip install pyinstaller")
        sys.exit(1)
    
    print("\nThis will build:")
    print("  1. PTPD Viewer (for end-users)")
    print("  2. PTPD Creator (for admin/sellers)")
    
    response = input("\nContinue? [Y/n]: ").strip().lower()
    if response and response != 'y':
        print("Build cancelled.")
        sys.exit(0)
    
    # Build both
    success_viewer = build_viewer()
    success_creator = build_creator()
    
    if success_viewer and success_creator:
        create_distribution_package()
        
        print("\n" + "="*60)
        print("🎉 BUILD COMPLETE!")
        print("="*60)
        print("\nExecutables created in 'dist/' folder:")
        print("  ✅ PTPD-Viewer.exe  (for distribution to end-users)")
        print("  ✅ PTPD-Creator.exe (for your use)")
        print("\nDistribution packages in 'distribution/' folder:")
        print("  📦 PTPD-Viewer/     (ready to distribute)")
        print("  📦 PTPD-Creator/    (keep for yourself)")
        print("\nNext steps:")
        print("  1. Test both executables")
        print("  2. Create installer (optional)")
        print("  3. Distribute to users")
        print("="*60)
    else:
        print("\n❌ Build failed. Check errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
