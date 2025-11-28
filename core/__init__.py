# core/__init__.py
"""
PTDP Core Module
Protected Digital Product Format - Core Functionality
"""

from .creator import PTDPCreator
from .reader import PTDPReader
from .license import LicenseValidator
from .hwid import HardwareID

__version__ = "1.0.0"
__all__ = ['PTDPCreator', 'PTDPReader', 'LicenseValidator', 'HardwareID']
