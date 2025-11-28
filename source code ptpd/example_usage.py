#!/usr/bin/env python3
"""
Example Usage - PTPD Protection System
Demonstrasi lengkap cara menggunakan PTPD system
"""

import os
import sys

# Add to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.creator import PTPDCreator
from core.reader import PTPDReader
from core.license import LicenseValidator
from core.hwid import HardwareID

def example_1_protect_file():
    """Example: Protect a file"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Protect a Digital Product")
    print("="*60)
    
    # Create a sample file to protect
    sample_file = "sample_ebook.txt"
    with open(sample_file, 'w') as f:
        f.write("This is a sample ebook content.\n")
        f.write("Chapter 1: Introduction to Trading\n")
        f.write("..." * 100)
    
    print(f"✅ Created sample file: {sample_file}")
    
    # Protect it
    creator = PTPDCreator()
    
    config = {
        'product_id': 'EBOOK001',
        'product_name': 'Advanced Trading Guide',
        'version': '1.0',
        'license_type': 'premium',
        'master_password': 'MySecretPassword123',
        'require_online': False,
        'max_devices': 1,
        'expiry_date': None,  # Lifetime
        'view_limit': None,   # Unlimited views
    }
    
    result = creator.create_protected_file(
        input_file=sample_file,
        output_file='sample_ebook.ptpd',
        config=config
    )
    
    if result['success']:
        print(f"\n✅ Protected file created: {result['output_file']}")
        print(f"🆔 Product ID: {result['product_id']}")
        print(f"📊 Size: {result['protected_size'] / 1024:.2f} KB")
    
    return result

def example_2_generate_license():
    """Example: Generate license key"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Generate License Key")
    print("="*60)
    
    # Get buyer's device ID (they send this to you)
    buyer_device_id = HardwareID.get_simple_hwid()
    print(f"Buyer's Device ID: {buyer_device_id[:16]}...")
    
    # Generate license
    license_key = LicenseValidator.generate_license(
        product_id='EBOOK001',
        hwid=buyer_device_id,
        expiry_date='LIFETIME'
    )
    
    print(f"\n🔑 License Key Generated:")
    print(f"   {license_key}")
    print(f"\n📧 Send this to the buyer!")
    
    return license_key

def example_3_open_protected_file(license_key):
    """Example: Open protected file with license"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Open Protected File")
    print("="*60)
    
    reader = PTPDReader()
    
    # First, read metadata
    metadata = reader.read_metadata('sample_ebook.ptpd')
    print(f"\n📦 Product: {metadata['product_name']}")
    print(f"🆔 Product ID: {metadata['product_id']}")
    
    # Decrypt with license
    result = reader.decrypt_file(
        ptpd_file='sample_ebook.ptpd',
        license_key=license_key,
        output_file='sample_ebook_decrypted.txt'
    )
    
    if result['success']:
        print(f"\n✅ File decrypted successfully!")
        print(f"📁 Output: {result['output_file']}")
        
        # Show decrypted content
        with open(result['output_file'], 'r') as f:
            print(f"\n📄 Content preview:")
            print(f.read()[:200] + "...")
    else:
        print(f"\n❌ Failed: {result['error']}")
    
    return result

def example_4_device_locked_license():
    """Example: Generate device-locked license"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Device-Locked License")
    print("="*60)
    
    # Specific buyer's HWID (they must send this to you)
    specific_hwid = "A1B2C3D4E5F6G7H8"
    
    license_key = LicenseValidator.generate_license(
        product_id='EBOOK001',
        hwid=specific_hwid,
        expiry_date='20251231'  # Expires Dec 31, 2025
    )
    
    print(f"🔒 Device-Locked License:")
    print(f"   License: {license_key}")
    print(f"   Locked to HWID: {specific_hwid}")
    print(f"   Expires: 2025-12-31")
    print(f"\n⚠️  This license ONLY works on device: {specific_hwid}")
    
    return license_key

def example_5_any_device_license():
    """Example: License for any device (less secure)"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Any-Device License")
    print("="*60)
    
    license_key = LicenseValidator.generate_license(
        product_id='EBOOK001',
        hwid=None,  # No device lock
        expiry_date='LIFETIME'
    )
    
    print(f"🔓 Any-Device License (less secure):")
    print(f"   {license_key}")
    print(f"\n⚠️  This license works on ANY device!")
    print(f"   Use only for trusted buyers or testing.")
    
    return license_key

def example_6_batch_protect():
    """Example: Batch protect multiple files"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Batch Protection")
    print("="*60)
    
    # Create sample files
    files = []
    for i in range(1, 4):
        filename = f"chapter_{i}.txt"
        with open(filename, 'w') as f:
            f.write(f"Chapter {i} content...\n" * 50)
        files.append(filename)
        print(f"✅ Created: {filename}")
    
    # Batch protect
    creator = PTPDCreator()
    
    config_template = {
        'master_password': 'MySecretPassword123',
        'require_online': False,
        'max_devices': 1,
        'license_type': 'premium'
    }
    
    result = creator.batch_protect(
        input_files=files,
        output_dir='protected_chapters',
        config_template=config_template
    )
    
    print(f"\n✅ Batch protection complete!")
    print(f"   Success: {result['success']}/{result['total']}")
    print(f"   Output: protected_chapters/")

def cleanup():
    """Cleanup sample files"""
    import glob
    
    files_to_remove = [
        'sample_ebook.txt',
        'sample_ebook.ptpd',
        'sample_ebook_decrypted.txt',
        'chapter_*.txt'
    ]
    
    for pattern in files_to_remove:
        for file in glob.glob(pattern):
            try:
                os.remove(file)
            except:
                pass
    
    # Remove directory
    import shutil
    if os.path.exists('protected_chapters'):
        shutil.rmtree('protected_chapters')

def main():
    """Run all examples"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "PTPD PROTECTION SYSTEM EXAMPLES" + " "*17 + "║")
    print("╚" + "="*58 + "╝")
    
    print("\nThis will demonstrate:")
    print("  1. Protecting a file")
    print("  2. Generating license keys")
    print("  3. Opening protected files")
    print("  4. Device-locked licenses")
    print("  5. Any-device licenses")
    print("  6. Batch protection")
    
    input("\nPress Enter to start...")
    
    # Run examples
    result1 = example_1_protect_file()
    license2 = example_2_generate_license()
    result3 = example_3_open_protected_file(license2)
    license4 = example_4_device_locked_license()
    license5 = example_5_any_device_license()
    example_6_batch_protect()
    
    print("\n" + "="*60)
    print("✅ All examples completed!")
    print("="*60)
    
    # Cleanup
    response = input("\nCleanup sample files? [Y/n]: ").strip().lower()
    if not response or response == 'y':
        cleanup()
        print("✅ Cleanup complete!")

if __name__ == "__main__":
    main()
