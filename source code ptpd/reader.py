# core/reader.py
"""
PTPD Reader Module
Decrypt and open protected digital products
"""

import json
import base64
import hashlib
import os
import tempfile
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from .license import LicenseValidator
from .hwid import HardwareID

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class PTPDReader:
    """Read and decrypt .ptpd files"""
    
    MAGIC_BYTES = config.MAGIC_BYTES
    
    def __init__(self):
        self.validator = LicenseValidator()
        self.hwid = HardwareID.get_simple_hwid()
        self.usage_file = config.USAGE_FILE
        
        # Ensure usage file directory exists
        os.makedirs(os.path.dirname(self.usage_file), exist_ok=True)
    
    def read_metadata(self, ptpd_file):
        """
        Baca metadata tanpa decrypt content
        
        Args:
            ptpd_file: Path ke .ptpd file
        
        Returns:
            dict: Metadata information
        """
        if not os.path.exists(ptpd_file):
            raise FileNotFoundError(f"File not found: {ptpd_file}")
        
        with open(ptpd_file, 'rb') as f:
            # Validate header
            magic = f.read(4)
            if magic != self.MAGIC_BYTES:
                raise ValueError("Invalid PTPD file format! This is not a valid .ptpd file.")
            
            version = f.read(3)
            
            # Read metadata
            meta_len = int.from_bytes(f.read(4), 'big')
            meta_json = f.read(meta_len)
            metadata = json.loads(meta_json.decode())
        
        return metadata
    
    def decrypt_file(self, ptpd_file, license_key, output_file=None, master_password=None):
        """
        Decrypt .ptpd file dengan validasi license
        
        Args:
            ptpd_file: Path ke .ptpd file
            license_key: License key dari user
            output_file: Path output file (None = return content in memory)
            master_password: Master password (None = derive from license)
        
        Returns:
            dict: Result dengan success status dan content/path
        """
        print(f"🔓 Opening protected file: {ptpd_file}")
        
        if not os.path.exists(ptpd_file):
            return {
                'success': False,
                'error': f'File not found: {ptpd_file}'
            }
        
        try:
            # 1. Read file structure
            with open(ptpd_file, 'rb') as f:
                # Header
                magic = f.read(4)
                if magic != self.MAGIC_BYTES:
                    return {
                        'success': False,
                        'error': 'Invalid PTPD file format'
                    }
                
                version = f.read(3)
                
                # Metadata
                meta_len = int.from_bytes(f.read(4), 'big')
                meta_json = f.read(meta_len)
                metadata = json.loads(meta_json.decode())
                
                # Encrypted content
                content_len = int.from_bytes(f.read(8), 'big')
                encrypted_content = f.read(content_len)
                
                # Integrity check
                expected_integrity = f.read(32)
                actual_integrity = hashlib.sha256(
                    magic + version + meta_json + encrypted_content
                ).digest()
                
                if expected_integrity != actual_integrity:
                    return {
                        'success': False,
                        'error': 'File integrity check failed! File may be corrupted or tampered.'
                    }
            
            print(f"📦 Product: {metadata['product_name']}")
            print(f"🆔 Product ID: {metadata['product_id']}")
            print(f"📄 Type: {metadata['original_extension']}")
            
            # 2. Validate license
            print("🔍 Validating license...")
            
            if metadata.get('require_online', False):
                valid, message = self.validator.validate_online(
                    license_key, 
                    metadata['product_id']
                )
            else:
                valid, message = self.validator.validate_offline(
                    license_key,
                    metadata['product_id']
                )
            
            if not valid:
                return {
                    'success': False,
                    'error': f'License validation failed: {message}'
                }
            
            print(f"✅ License validated: {message}")
            
            # 3. Check expiry date from metadata
            if metadata.get('expiry_date'):
                try:
                    exp_date = datetime.fromisoformat(metadata['expiry_date'])
                    if datetime.now() > exp_date:
                        return {
                            'success': False,
                            'error': f'Product license expired on {exp_date.strftime("%Y-%m-%d")}'
                        }
                except:
                    pass
            
            # 4. Check view limit
            if config.ENABLE_VIEW_LIMIT and metadata.get('view_limit'):
                usage_count = self._get_usage_count(metadata['product_id'])
                if usage_count >= metadata['view_limit']:
                    return {
                        'success': False,
                        'error': f"View limit reached ({metadata['view_limit']} views maximum)"
                    }
                print(f"📊 Views: {usage_count + 1}/{metadata['view_limit']}")
                self._increment_usage(metadata['product_id'])
            
            # 5. Decrypt content
            print("🔓 Decrypting content...")
            
            try:
                # Use master password or derive from license
                if master_password is None:
                    master_password = license_key
                
                # Get salt from metadata
                salt = base64.b64decode(metadata['salt'])
                
                # Generate decryption key
                kdf = PBKDF2(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=config.KDF_ITERATIONS,
                )
                key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
                
                # Decrypt
                fernet = Fernet(key)
                decrypted_content = fernet.decrypt(encrypted_content)
                
                # Verify file hash
                file_hash = hashlib.sha256(decrypted_content).hexdigest()
                if file_hash != metadata['file_hash']:
                    return {
                        'success': False,
                        'error': 'File corruption detected! Hash mismatch.'
                    }
                
            except Exception as e:
                return {
                    'success': False,
                    'error': f'Decryption failed: {str(e)}\nCheck your license key or master password.'
                }
            
            print(f"✅ Decryption successful!")
            print(f"📄 File size: {len(decrypted_content) / 1024:.2f} KB")
            
            # 6. Save or return content
            if output_file:
                # Save to file
                with open(output_file, 'wb') as f:
                    f.write(decrypted_content)
                print(f"💾 Saved to: {output_file}")
                
                return {
                    'success': True,
                    'output_file': output_file,
                    'metadata': metadata,
                    'size': len(decrypted_content)
                }
            else:
                # Return in memory (untuk viewer)
                return {
                    'success': True,
                    'content': decrypted_content,
                    'metadata': metadata,
                    'size': len(decrypted_content)
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'Error reading file: {str(e)}'
            }
    
    def _get_usage_count(self, product_id):
        """Get usage count untuk view limit tracking"""
        if not os.path.exists(self.usage_file):
            return 0
        
        try:
            with open(self.usage_file, 'r') as f:
                usage = json.load(f)
                return usage.get(product_id, 0)
        except:
            return 0
    
    def _increment_usage(self, product_id):
        """Increment usage counter"""
        usage = {}
        if os.path.exists(self.usage_file):
            try:
                with open(self.usage_file, 'r') as f:
                    usage = json.load(f)
            except:
                pass
        
        usage[product_id] = usage.get(product_id, 0) + 1
        
        with open(self.usage_file, 'w') as f:
            json.dump(usage, f, indent=2)
    
    def get_file_info(self, ptpd_file):
        """Get detailed information about .ptpd file"""
        try:
            metadata = self.read_metadata(ptpd_file)
            file_size = os.path.getsize(ptpd_file)
            
            info = {
                'file_path': ptpd_file,
                'file_size': file_size,
                'product_name': metadata['product_name'],
                'product_id': metadata['product_id'],
                'version': metadata.get('version', 'N/A'),
                'license_type': metadata.get('license_type', 'N/A'),
                'original_extension': metadata['original_extension'],
                'original_size': metadata['file_size'],
                'created_at': metadata['created_at'],
                'require_online': metadata.get('require_online', False),
                'max_devices': metadata.get('max_devices', 1),
                'expiry_date': metadata.get('expiry_date', 'N/A'),
                'view_limit': metadata.get('view_limit', 'Unlimited'),
                'has_watermark': bool(metadata.get('watermark', ''))
            }
            
            return info
        except Exception as e:
            return {'error': str(e)}

# ========================
# CLI Interface
# ========================

def decrypt_file_cli():
    """Command-line interface untuk decrypt file"""
    print("🔓 PTPD File Decryption Tool")
    print("=" * 50)
    
    # Input file
    ptpd_file = input("PTPD file path: ").strip()
    if not os.path.exists(ptpd_file):
        print(f"❌ File not found: {ptpd_file}")
        return
    
    # Show metadata first
    reader = PTPDReader()
    try:
        metadata = reader.read_metadata(ptpd_file)
        print(f"\n📦 Product: {metadata['product_name']}")
        print(f"🆔 Product ID: {metadata['product_id']}")
        print(f"📄 Type: {metadata['original_extension']}")
        print(f"💎 License Type: {metadata.get('license_type', 'N/A')}")
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return
    
    # License key
    print("\n" + "-" * 50)
    license_key = input("Enter license key: ").strip()
    
    # Output file
    default_output = ptpd_file.replace('.ptpd', metadata['original_extension'])
    output_file = input(f"Output file [{default_output}]: ").strip()
    if not output_file:
        output_file = default_output
    
    # Decrypt
    print("\n" + "=" * 50)
    result = reader.decrypt_file(ptpd_file, license_key, output_file)
    
    if result['success']:
        print("\n🎉 SUCCESS!")
        print(f"📁 Decrypted file: {result['output_file']}")
        print(f"📊 Size: {result['size'] / 1024:.2f} KB")
    else:
        print(f"\n❌ FAILED: {result['error']}")

if __name__ == "__main__":
    decrypt_file_cli()
