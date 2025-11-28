#!/usr/bin/env python3
"""
PTDP Creator - Entry Point
Protect PDF files and generate license keys

This is a standalone entry point that ensures all dependencies are properly loaded.
"""

import sys
import os

# Ensure cryptography is available first (before any other imports)
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError as e:
    print(f"Error: Missing cryptography module - {e}")
    print("Please install: pip install cryptography")
    input("Press Enter to exit...")
    sys.exit(1)

# Now import and run the creator
from gui.creator import main

if __name__ == "__main__":
    main()
