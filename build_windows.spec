# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for Windows executables
Builds both Creator and Viewer for Windows
"""

# PTDP Viewer (User App)
viewer_a = Analysis(
    ['gui/viewer_modern.py'],
    pathex=[],
    binaries=[],
    datas=[('config.py', '.')],
    hiddenimports=[
        'cryptography',
        'cryptography.fernet',
        'cryptography.hazmat.primitives.kdf.pbkdf2',
        'cryptography.hazmat.backends',
        'Crypto.Cipher.AES',
        'customtkinter',
        'PIL',
        'psutil',
        'core.reader',
        'core.license',
        'core.hwid',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'pandas'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

viewer_pyz = PYZ(viewer_a.pure, viewer_a.zipped_data, cipher=None)

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
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# PTDP Creator (Seller App)
creator_a = Analysis(
    ['gui/creator.py'],
    pathex=[],
    binaries=[],
    datas=[('config.py', '.')],
    hiddenimports=[
        'cryptography',
        'cryptography.fernet',
        'cryptography.hazmat.primitives.kdf.pbkdf2',
        'cryptography.hazmat.backends',
        'Crypto.Cipher.AES',
        'hashlib',
        'secrets',
        'core.creator',
        'core.license',
        'core.hwid',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'pandas'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

creator_pyz = PYZ(creator_a.pure, creator_a.zipped_data, cipher=None)

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
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
