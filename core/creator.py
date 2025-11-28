# core/creator.py
"""
PTDP Creator Module
Protect and encrypt digital products
"""

import json
import base64
import hashlib
import os
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class PTDPCreator:
    """Create protected .ptdp files"""
    
    MAGIC_BYTES = config.MAGIC_BYTES
    VERSION = config.VERSION
    
    def __init__(self):
        self.salt = os.urandom(16)
    
    def create_protected_file(self, input_file, output_file, protection_config):
        """
        Protect file dengan enkripsi dan metadata
        
        Args:
            input_file: Path ke file yang mau diprotect
            output_file: Path output .ptdp file
            protection_config: Dict berisi configuration
            
        Config Structure:
        {
            'product_id': 'EBOOK001',              # Required
            'product_name': 'Trading Guide',        # Required
            'version': '1.0',                       # Optional
            'license_type': 'premium',              # Optional
            'master_password': 'secret123',         # Required
            'require_online': False,                # Optional
            'max_devices': 1,                       # Optional
            'expiry_date': '2025-12-31',           # Optional (ISO format atau None)
            'allow_print': False,                   # Optional
            'allow_copy': False,                    # Optional
            'view_limit': None,                     # Optional (None = unlimited)
            'watermark': 'Licensed to {buyer}'      # Optional
        }
        
        Returns:
            dict: Result dengan success status dan info
        """
        
        print(f"🔒 Protecting file: {input_file}")
        
        # Validate input file
        if not os.path.exists(input_file):
            return {
                'success': False,
                'error': f'Input file not found: {input_file}'
            }
        
        # Check file size
        file_size = os.path.getsize(input_file)
        if file_size > config.MAX_FILE_SIZE:
            return {
                'success': False,
                'error': f'File too large. Max size: {config.MAX_FILE_SIZE / (1024*1024):.0f} MB'
            }
        
        # Check extension
        ext = os.path.splitext(input_file)[1].lower()
        if ext not in config.ALLOWED_EXTENSIONS:
            print(f"⚠️  Warning: Extension {ext} not in allowed list")
        
        try:
            # 1. Read original file
            with open(input_file, 'rb') as f:
                original_content = f.read()
            
            file_hash = hashlib.sha256(original_content).hexdigest()
            print(f"📄 File size: {len(original_content) / 1024:.2f} KB")
            print(f"🔐 SHA256: {file_hash[:16]}...")
            
            # 2. Generate encryption key from master password
            master_password = protection_config.get('master_password')
            if not master_password:
                return {
                    'success': False,
                    'error': 'Master password required in config'
                }
            
            # Use product_id + secret_key for consistent encryption
            # This ensures the same key is used for encryption and decryption
            encryption_password = f"{protection_config['product_id']}:{config.SECRET_KEY}"
            
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=self.salt,
                iterations=config.KDF_ITERATIONS,
            )
            key = base64.urlsafe_b64encode(
                kdf.derive(encryption_password.encode())
            )
            
            # 3. Encrypt content
            print("🔐 Encrypting content...")
            fernet = Fernet(key)
            encrypted_content = fernet.encrypt(original_content)
            
            # 4. Prepare metadata
            metadata = {
                # Required fields
                'product_id': protection_config['product_id'],
                'product_name': protection_config['product_name'],
                
                # Optional fields with defaults
                'version': protection_config.get('version', '1.0'),
                'license_type': protection_config.get('license_type', config.DEFAULT_LICENSE_TYPE),
                'require_online': protection_config.get('require_online', False),
                'max_devices': protection_config.get('max_devices', config.DEFAULT_MAX_DEVICES),
                'expiry_date': protection_config.get('expiry_date', None),
                'allow_print': protection_config.get('allow_print', False),
                'allow_copy': protection_config.get('allow_copy', False),
                'view_limit': protection_config.get('view_limit', None),
                'watermark': protection_config.get('watermark', ''),
                
                # Auto-generated fields
                'original_extension': ext,
                'file_size': len(original_content),
                'file_hash': file_hash,
                'created_at': datetime.now().isoformat(),
                'salt': base64.b64encode(self.salt).decode(),
                'encrypted_size': len(encrypted_content)
            }
            
            meta_json = json.dumps(metadata, indent=2).encode()
            
            # 5. Write .ptdp file
            print(f"💾 Writing protected file: {output_file}")
            
            with open(output_file, 'wb') as f:
                # Write header
                f.write(self.MAGIC_BYTES)
                f.write(self.VERSION)
                
                # Write metadata section
                f.write(len(meta_json).to_bytes(4, 'big'))
                f.write(meta_json)
                
                # Write encrypted content section
                f.write(len(encrypted_content).to_bytes(8, 'big'))
                f.write(encrypted_content)
                
                # Write integrity check (SHA256 of everything)
                integrity = hashlib.sha256(
                    self.MAGIC_BYTES + self.VERSION + meta_json + encrypted_content
                ).digest()
                f.write(integrity)
            
            output_size = os.path.getsize(output_file)
            
            print(f"✅ Protected file created successfully!")
            print(f"📦 Output size: {output_size / 1024:.2f} KB")
            print(f"🔐 Product ID: {metadata['product_id']}")
            print(f"🆔 Requires license key to unlock")
            
            return {
                'success': True,
                'output_file': output_file,
                'product_id': metadata['product_id'],
                'file_hash': file_hash,
                'original_size': len(original_content),
                'protected_size': output_size,
                'metadata': metadata
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'Protection failed: {str(e)}'
            }
    
    def batch_protect(self, input_files, output_dir, config_template):
        """
        Protect multiple files dengan config yang sama
        
        Args:
            input_files: List of file paths
            output_dir: Output directory
            config_template: Base config untuk semua files
        
        Returns:
            dict: Batch results
        """
        os.makedirs(output_dir, exist_ok=True)
        
        results = []
        success_count = 0
        
        print(f"📦 Batch protecting {len(input_files)} files...")
        print("=" * 50)
        
        for i, input_file in enumerate(input_files, 1):
            print(f"\n[{i}/{len(input_files)}] Processing: {os.path.basename(input_file)}")
            
            # Create unique product_id for each file
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            config = config_template.copy()
            config['product_name'] = base_name
            
            if 'product_id' not in config:
                config['product_id'] = f"PROD{i:03d}"
            
            # Output filename
            output_file = os.path.join(output_dir, base_name + '.ptdp')
            
            # Protect
            result = self.create_protected_file(input_file, output_file, config)
            results.append(result)
            
            if result['success']:
                success_count += 1
        
        print("\n" + "=" * 50)
        print(f"✅ Batch complete: {success_count}/{len(input_files)} successful")
        
        return {
            'total': len(input_files),
            'success': success_count,
            'failed': len(input_files) - success_count,
            'results': results
        }

# ========================
# CLI Interface
# ========================

def create_protected_cli():
    """Command-line interface untuk create protected file"""
    print("🔒 PTDP File Protection Tool")
    print("=" * 50)
    
    # Input file
    input_file = input("Input file path: ").strip()
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        return
    
    # Output file
    default_output = os.path.splitext(input_file)[0] + '.ptdp'
    output_file = input(f"Output file [{default_output}]: ").strip()
    if not output_file:
        output_file = default_output
    
    # Product info
    print("\n--- Product Information ---")
    product_id = input("Product ID (e.g., EBOOK001): ").strip()
    product_name = input("Product Name: ").strip()
    master_password = input("Master Password (keep this secret!): ").strip()
    
    # Options
    print("\n--- Protection Options ---")
    require_online = input("Require online validation? [y/N]: ").strip().lower() == 'y'
    max_devices = int(input("Max devices [1]: ").strip() or "1")
    
    expiry_input = input("Expiry date (YYYY-MM-DD) or leave empty for lifetime: ").strip()
    expiry_date = expiry_input if expiry_input else None
    
    # Create config
    config = {
        'product_id': product_id,
        'product_name': product_name,
        'master_password': master_password,
        'require_online': require_online,
        'max_devices': max_devices,
        'expiry_date': expiry_date
    }
    
    # Protect file
    print("\n" + "=" * 50)
    creator = PTDPCreator()
    result = creator.create_protected_file(input_file, output_file, config)
    
    if result['success']:
        print("\n🎉 SUCCESS!")
        print(f"\n📁 Protected file: {result['output_file']}")
        print(f"🆔 Product ID: {result['product_id']}")
        print(f"\n⚠️  IMPORTANT: Keep your master password safe!")
        print(f"   Master Password: {master_password}")
    else:
        print(f"\n❌ FAILED: {result['error']}")

if __name__ == "__main__":
    create_protected_cli()
