#!/usr/bin/env python3
"""
PTDP Creator - Entry Point
Protect PDF files and generate license keys

This entry point pre-imports all required modules to ensure
PyInstaller bundles them correctly.
"""

import sys
import os

# ============================================================
# PRE-IMPORT ALL REQUIRED MODULES
# This ensures PyInstaller bundles everything correctly
# ============================================================

# Standard library (should always be available)
import json
import hashlib
import base64
import uuid
import platform
import tempfile
from datetime import datetime
from pathlib import Path

# Third-party dependencies - MUST be bundled
try:
    # Cryptography
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    
    # Requests (for license validation)
    import requests
    
    # PSUtil (for hardware ID)
    import psutil
    
    # CustomTkinter (for UI)
    import customtkinter
    
    # PIL/Pillow
    from PIL import Image
    
except ImportError as e:
    import tkinter.messagebox as mb
    mb.showerror("Missing Module", f"Required module not found: {e}\n\nPlease reinstall the application.")
    sys.exit(1)

# ============================================================
# START APPLICATION
# ============================================================

from gui.creator import main

if __name__ == "__main__":
    main()
