# build.py
"""
Build script untuk compile PTDP tools menjadi executables
Requires: pip install pyinstaller
"""

import PyInstaller.__main__
import os
import sys
import shutil

def build_viewer():
    """Build PTDP Viewer untuk end-users"""
    print("\n" + "="*60)
    print("🔨 Building PTDP Viewer (End-User Application)")
    print("="*60)
    
    args = [
        'gui/viewer.py',
        '--name=PTDP-Viewer',
        '--onefile',
        '--windowed',
        '--clean',
        '--noconfirm',
        '--paths=.',  # Add root path
        # Add hidden imports
        '--hidden-import=cryptography',
        '--hidden-import=cryptography.fernet',
        '--hidden-import=cryptography.hazmat',
        '--hidden-import=cryptography.hazmat.primitives',
        '--hidden-import=requests',
        '--hidden-import=psutil',
        '--hidden-import=core',
        '--hidden-import=core.reader',
        '--hidden-import=core.license',
        '--hidden-import=core.hwid',
    ]
    
    # Add icon if exists
    if os.path.exists('assets/icon.ico'):
        args.append('--icon=assets/icon.ico')
    
    try:
        PyInstaller.__main__.run(args)
        print("\n✅ PTDP Viewer built successfully!")
        print(f"   Location: dist/PTDP-Viewer.exe")
    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        return False
    
    return True

def build_creator():
    """Build PTDP Creator untuk admin/sellers"""
    print("\n" + "="*60)
    print("🔨 Building PTDP Creator (Admin Tool)")
    print("="*60)
    
    args = [
        'gui/creator.py',
        '--name=PTDP-Creator',
        '--onefile',
        '--windowed',
        '--clean',
        '--noconfirm',
        '--paths=.',  # Add root path
        '--hidden-import=cryptography',
        '--hidden-import=cryptography.fernet',
        '--hidden-import=cryptography.hazmat',
        '--hidden-import=cryptography.hazmat.primitives',
        '--hidden-import=core',
        '--hidden-import=core.creator',
        '--hidden-import=core.license',
    ]
    
    if os.path.exists('assets/icon.ico'):
        args.append('--icon=assets/icon.ico')
    
    try:
        PyInstaller.__main__.run(args)
        print("\n✅ PTDP Creator built successfully!")
        print(f"   Location: dist/PTDP-Creator.exe")
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
    dist_viewer = 'distribution/PTDP-Viewer'
    dist_creator = 'distribution/PTDP-Creator'
    
    os.makedirs(dist_viewer, exist_ok=True)
    os.makedirs(dist_creator, exist_ok=True)
    
    # Copy viewer
    if os.path.exists('dist/PTDP-Viewer.exe'):
        shutil.copy('dist/PTDP-Viewer.exe', dist_viewer)
        print("✅ Copied PTDP-Viewer.exe")
    
    # Copy creator
    if os.path.exists('dist/PTDP-Creator.exe'):
        shutil.copy('dist/PTDP-Creator.exe', dist_creator)
        print("✅ Copied PTDP-Creator.exe")
    
    # Create README for viewer
    viewer_readme = f"""
PTDP Viewer - User Guide
========================

WHAT IS THIS?
This application allows you to open protected .ptdp files.

HOW TO INSTALL:
1. Copy PTDP-Viewer.exe to any folder (e.g., C:\\Program Files\\PTDP Viewer)
2. Run PTDP-Viewer.exe
3. (Optional) Run register_ptdp.bat as Administrator to associate .ptdp files

HOW TO USE:
1. Open PTDP-Viewer.exe
2. Click "Open PTDP File" and select your .ptdp file
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

© 2024 PTDP Protection System
"""
    
    with open(f'{dist_viewer}/README.txt', 'w') as f:
        f.write(viewer_readme)
    print("✅ Created README.txt for viewer")
    
    # Create README for creator
    creator_readme = f"""
PTDP Creator - Admin Guide
===========================

WHAT IS THIS?
This tool allows you to protect your digital products with .ptdp format.

HOW TO USE:
1. Run PTDP-Creator.exe
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

© 2024 PTDP Protection System
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
    print("║" + " "*15 + "PTDP BUILD SYSTEM" + " "*25 + "║")
    print("╚" + "="*58 + "╝")
    
    # Check if pyinstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("\n❌ PyInstaller not found!")
        print("   Install it with: pip install pyinstaller")
        sys.exit(1)
    
    print("\nThis will build:")
    print("  1. PTDP Viewer (for end-users)")
    print("  2. PTDP Creator (for admin/sellers)")
    
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
        print("  ✅ PTDP-Viewer.exe  (for distribution to end-users)")
        print("  ✅ PTDP-Creator.exe (for your use)")
        print("\nDistribution packages in 'distribution/' folder:")
        print("  📦 PTDP-Viewer/     (ready to distribute)")
        print("  📦 PTDP-Creator/    (keep for yourself)")
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
