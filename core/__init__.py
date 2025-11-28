# core/__init__.py
"""
PTDP Core Module
Protected Digital Product Format - Core Functionality

Note: Imports are done lazily to avoid circular import issues
when bundled with PyInstaller. Import specific classes directly:
  from core.creator import PTDPCreator
  from core.reader import PTDPReader
  from core.license import LicenseValidator
  from core.hwid import HardwareID
"""

__version__ = "1.0.0"

# Lazy imports - only when accessed
def __getattr__(name):
    if name == 'PTDPCreator':
        from .creator import PTDPCreator
        return PTDPCreator
    elif name == 'PTDPReader':
        from .reader import PTDPReader
        return PTDPReader
    elif name == 'LicenseValidator':
        from .license import LicenseValidator
        return LicenseValidator
    elif name == 'HardwareID':
        from .hwid import HardwareID
        return HardwareID
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ['PTDPCreator', 'PTDPReader', 'LicenseValidator', 'HardwareID']
