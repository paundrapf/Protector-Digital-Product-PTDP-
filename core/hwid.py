# core/hwid.py
"""
Hardware ID Detection Module
Generates unique hardware identifier for device locking
"""

import hashlib
import uuid
import platform
import psutil

class HardwareID:
    """Hardware ID detection untuk device locking"""
    
    @staticmethod
    def get_hwid():
        """Generate unique hardware ID dari komponen sistem (detailed)"""
        try:
            # CPU Info
            cpu_info = platform.processor()
            
            # MAC Address
            mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                           for elements in range(0,2*6,2)][::-1])
            
            # System info
            system_info = f"{platform.system()}-{platform.machine()}-{platform.release()}"
            
            # Disk info (if available)
            try:
                if platform.system() == 'Windows':
                    import wmi
                    c = wmi.WMI()
                    disk_id = c.Win32_DiskDrive()[0].SerialNumber.strip()
                else:
                    disk_id = "UNIX"
            except:
                disk_id = "UNKNOWN"
            
            # Combine semua info
            hwid_string = f"{cpu_info}-{mac}-{disk_id}-{system_info}"
            
            # Hash untuk privacy
            hwid_hash = hashlib.sha256(hwid_string.encode()).hexdigest()
            
            return hwid_hash
        except Exception as e:
            print(f"⚠️  Warning: Could not generate detailed HWID: {e}")
            return HardwareID.get_simple_hwid()
    
    @staticmethod
    def get_simple_hwid():
        """Versi simple untuk cross-platform compatibility"""
        try:
            # MAC Address (most reliable)
            mac = hex(uuid.getnode())[2:]
            
            # System info
            system = f"{platform.system()}{platform.machine()}"
            
            # Combine
            combined = f"{mac}-{system}"
            
            # Hash
            hwid_hash = hashlib.sha256(combined.encode()).hexdigest()
            
            return hwid_hash[:32]  # First 32 chars
        except Exception as e:
            # Fallback to UUID
            return str(uuid.uuid4()).replace('-', '')[:32]
    
    @staticmethod
    def get_system_info():
        """Get detailed system information for debugging"""
        info = {
            'platform': platform.system(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
            'mac_address': hex(uuid.getnode())[2:],
            'hwid': HardwareID.get_simple_hwid()
        }
        return info

if __name__ == "__main__":
    # Test hardware ID generation
    print("🖥️  Hardware ID Detection Test")
    print("=" * 50)
    
    hwid = HardwareID.get_simple_hwid()
    print(f"✅ Hardware ID: {hwid}")
    
    info = HardwareID.get_system_info()
    print(f"\n📊 System Info:")
    for key, value in info.items():
        print(f"  {key}: {value}")
