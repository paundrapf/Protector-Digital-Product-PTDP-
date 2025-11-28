# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for PTDP Viewer Modern (End-User App)
Builds a standalone executable for end users
"""

block_cipher = None

a = Analysis(
    ['gui/viewer_modern.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.py', '.'),
    ],
    hiddenimports=[
        'cryptography',
        'cryptography.fernet',
        'cryptography.hazmat.primitives.kdf.pbkdf2',
        'cryptography.hazmat.backends',
        'Crypto.Cipher.AES',
        'Crypto.Random',
        'Crypto.Util.Padding',
        'customtkinter',
        'PIL',
        'PIL._tkinter_finder',
        'hashlib',
        'secrets',
        'base64',
        'json',
        'datetime',
        'psutil',
        'core.reader',
        'core.license',
        'core.hwid',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'pytest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PTDP-Viewer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add your icon here if available
)
