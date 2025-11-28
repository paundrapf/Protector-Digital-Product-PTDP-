#!/usr/bin/env python3
"""
PTDP Sample Creator
Creates sample protected files and licenses for demonstration
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.creator import PTDPCreator
from core.license import LicenseValidator
from core.hwid import HardwareID

def create_sample_files():
    """Create sample protected files"""
    print("="*70)
    print("  PTDP SAMPLE CREATOR - Creating Demo Files")
    print("="*70)
    
    # Create samples directory
    samples_dir = "samples"
    os.makedirs(samples_dir, exist_ok=True)
    os.makedirs(os.path.join(samples_dir, "protected"), exist_ok=True)
    os.makedirs(os.path.join(samples_dir, "licenses"), exist_ok=True)
    
    creator = PTDPCreator()
    
    # Sample 1: Ebook (Lifetime, Any Device)
    print("\n📖 Sample 1: Ebook - Lifetime License, Any Device")
    print("-" * 70)
    
    ebook_config = {
        'product_id': 'EBOOK001',
        'product_name': 'Advanced Trading Strategies',
        'version': '1.0',
        'master_password': 'EbookSecret2024',
        'require_online': False,
        'max_devices': 1,
        'expiry_date': None,  # Lifetime
        'view_limit': None    # Unlimited
    }
    
    result1 = creator.create_protected_file(
        input_file=os.path.join(samples_dir, 'sample_ebook.txt'),
        output_file=os.path.join(samples_dir, 'protected', 'trading_ebook.ptdp'),
        protection_config=ebook_config
    )
    
    if result1['success']:
        # Generate license for any device
        license1 = LicenseValidator.generate_license(
            product_id='EBOOK001',
            hwid='ANYDEVIC',  # Works on any device
            expiry_date='LIFETIME'
        )
        
        # Save license info
        with open(os.path.join(samples_dir, 'licenses', 'ebook_license.txt'), 'w') as f:
            f.write("TRADING EBOOK LICENSE\n")
            f.write("="*50 + "\n\n")
            f.write(f"Product: {ebook_config['product_name']}\n")
            f.write(f"Product ID: {ebook_config['product_id']}\n")
            f.write(f"License Type: Lifetime, Any Device\n")
            f.write(f"License Key: {license1}\n\n")
            f.write("Master Password: EbookSecret2024\n")
            f.write("(This password is needed for decryption)\n")
        
        print(f"✅ Protected file: {result1['output_file']}")
        print(f"🔑 License key: {license1}")
        print(f"📝 License saved to: samples/licenses/ebook_license.txt")
    
    # Sample 2: Course (Device-Locked, 1 Year)
    print("\n\n🎓 Sample 2: Course - Device Locked, 1 Year Expiry")
    print("-" * 70)
    
    # Create course sample file
    course_content = """
    ╔══════════════════════════════════════════════════════════╗
    ║          PYTHON MASTERY COURSE - LESSON 1               ║
    ╚══════════════════════════════════════════════════════════╝
    
    Welcome to Python Mastery Course!
    
    This protected course includes:
    - 50+ Video lessons
    - Hands-on projects
    - Code examples
    - Lifetime support
    
    LESSON 1: Python Basics
    - Variables and data types
    - Control structures
    - Functions and modules
    
    [Course content would be here...]
    
    © 2024 Protected with PTDP System
    """
    
    with open(os.path.join(samples_dir, 'sample_course.txt'), 'w') as f:
        f.write(course_content)
    
    hwid = HardwareID.get_simple_hwid()
    
    course_config = {
        'product_id': 'COURSE01',
        'product_name': 'Python Mastery Course',
        'version': '2.0',
        'master_password': 'CoursePass2024',
        'require_online': False,
        'max_devices': 1,
        'expiry_date': '2025-12-31',
        'view_limit': 100
    }
    
    result2 = creator.create_protected_file(
        input_file=os.path.join(samples_dir, 'sample_course.txt'),
        output_file=os.path.join(samples_dir, 'protected', 'python_course.ptdp'),
        protection_config=course_config
    )
    
    if result2['success']:
        # Generate device-locked license
        license2 = LicenseValidator.generate_license(
            product_id='COURSE01',
            hwid=hwid,
            expiry_date='20251231'
        )
        
        with open(os.path.join(samples_dir, 'licenses', 'course_license.txt'), 'w') as f:
            f.write("PYTHON COURSE LICENSE\n")
            f.write("="*50 + "\n\n")
            f.write(f"Product: {course_config['product_name']}\n")
            f.write(f"Product ID: {course_config['product_id']}\n")
            f.write(f"License Type: Device Locked, 1 Year\n")
            f.write(f"Expiry Date: 2025-12-31\n")
            f.write(f"View Limit: 100 views\n")
            f.write(f"Device ID: {hwid[:16]}...\n")
            f.write(f"License Key: {license2}\n\n")
            f.write("Master Password: CoursePass2024\n")
            f.write("(This password is needed for decryption)\n")
        
        print(f"✅ Protected file: {result2['output_file']}")
        print(f"🔑 License key: {license2}")
        print(f"🖥️  Device locked to: {hwid[:16]}...")
        print(f"📝 License saved to: samples/licenses/course_license.txt")
    
    # Create README
    print("\n\n📄 Creating README...")
    print("-" * 70)
    
    readme = """# PTDP Sample Files

This directory contains sample protected files to demonstrate the PTDP system.

## Directory Structure

```
samples/
├── protected/              # Protected .ptdp files
│   ├── trading_ebook.ptdp
│   └── python_course.ptdp
├── licenses/               # License keys and info
│   ├── ebook_license.txt
│   └── course_license.txt
├── sample_ebook.txt       # Original file (for reference)
└── sample_course.txt      # Original file (for reference)
```

## How to Use

### Option 1: GUI Viewer
```bash
python -m gui.viewer
# Then open .ptdp file and enter license key
```

### Option 2: Command Line
```python
from core.reader import PTDPReader

reader = PTDPReader()
result = reader.decrypt_file(
    ptdp_file='samples/protected/trading_ebook.ptdp',
    license_key='[key from licenses/ebook_license.txt]',
    output_file='decrypted_ebook.txt',
    master_password='EbookSecret2024'
)
```

## Sample Files Information

### 1. Trading Ebook (trading_ebook.ptdp)
- **Product ID:** EBOOK001
- **License Type:** Lifetime, Any Device
- **Password:** EbookSecret2024
- **See:** `licenses/ebook_license.txt` for license key

### 2. Python Course (python_course.ptdp)
- **Product ID:** COURSE01
- **License Type:** Device Locked, 1 Year
- **Expiry:** 2025-12-31
- **View Limit:** 100 views
- **Password:** CoursePass2024
- **See:** `licenses/course_license.txt` for license key

## Notes

- The master password is required for decryption
- Device-locked licenses only work on the device they were generated for
- View limits are tracked locally
- Expired licenses cannot open files

## Testing

You can use these sample files to test:
- Opening protected files
- License validation
- Device locking
- Expiry dates
- View limits

Enjoy exploring the PTDP Protection System!
"""
    
    with open(os.path.join(samples_dir, 'README.md'), 'w') as f:
        f.write(readme)
    
    print("✅ README.md created")
    
    # Summary
    print("\n\n" + "="*70)
    print("  ✅ SAMPLE FILES CREATED SUCCESSFULLY!")
    print("="*70)
    print(f"\n📁 Location: {os.path.abspath(samples_dir)}/")
    print("\nCreated files:")
    print("  • samples/protected/trading_ebook.ptdp")
    print("  • samples/protected/python_course.ptdp")
    print("  • samples/licenses/ebook_license.txt")
    print("  • samples/licenses/course_license.txt")
    print("  • samples/README.md")
    
    print("\n🎯 Next Steps:")
    print("  1. Check license files for keys and passwords")
    print("  2. Test opening files with: python -m gui.viewer")
    print("  3. Or use programmatically as shown in samples/README.md")
    print("\n" + "="*70)

if __name__ == "__main__":
    create_sample_files()
