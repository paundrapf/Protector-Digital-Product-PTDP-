# -*- mode: python ; coding: utf-8 -*-
"""
PTDP Portable Windows Executables
Build standalone .exe files that work WITHOUT installation
User just downloads and runs - NO SETUP WIZARD NEEDED!
"""

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Common settings for both apps
common_excludes = [
    'matplotlib', 'numpy', 'pandas', 'scipy', 
    'PIL', 'sqlite3', 'test', 'unittest',
    'email', 'http', 'xml', 'pydoc',
]

common_hidden_imports = [
    'cryptography.hazmat.primitives.ciphers',
    'cryptography.hazmat.primitives.kdf.pbkdf2',
    'cryptography.hazmat.backends',
]

# ============================================================================
# PTDP VIEWER - For End Users (Portable)
# ============================================================================

viewer_a = Analysis(
    ['viewer.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('samples', 'samples'),  # Include sample files
    ],
    hiddenimports=common_hidden_imports + [
        'customtkinter',
        'PIL._tkinter_finder',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=common_excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

viewer_pyz = PYZ(
    viewer_a.pure, 
    viewer_a.zipped_data,
    cipher=block_cipher
)

viewer_exe = EXE(
    viewer_pyz,
    viewer_a.scripts,
    viewer_a.binaries,
    viewer_a.zipfiles,
    viewer_a.datas,
    [],
    name='PTDP-Viewer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Compress to reduce size
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon if you have one
)

# ============================================================================
# PTDP CREATOR - For Sellers (Portable)
# ============================================================================

creator_a = Analysis(
    ['creator.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('samples', 'samples'),
    ],
    hiddenimports=common_hidden_imports + [
        'customtkinter',
        'PIL._tkinter_finder',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=common_excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

creator_pyz = PYZ(
    creator_a.pure,
    creator_a.zipped_data,
    cipher=block_cipher
)

creator_exe = EXE(
    creator_pyz,
    creator_a.scripts,
    creator_a.binaries,
    creator_a.zipfiles,
    creator_a.datas,
    [],
    name='PTDP-Creator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

# Output both executables
COLLECT(
    viewer_exe,
    creator_exe,
    name='PTDP-Portable'
)
