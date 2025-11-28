# core/__init__.py
"""
PTPD Core Module
Protected Digital Product Format - Core Functionality
"""

from .creator import PTPDCreator
from .reader import PTPDReader
from .license import LicenseValidator
from .hwid import HardwareID

__version__ = "1.0.0"
__all__ = ['PTPDCreator', 'PTPDReader', 'LicenseValidator', 'HardwareID']
