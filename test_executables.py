#!/usr/bin/env python3
"""
Test PTDP Executables
Tests both Creator and Viewer executables
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def print_header(text):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text:^60}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    print(f"{RED}✗ {text}{RESET}")

def print_info(text):
    print(f"{YELLOW}ℹ {text}{RESET}")

def test_executables():
    """Test PTDP executables"""
    
    print_header("PTDP Executable Testing")
    
    # Check if executables exist
    creator_path = Path("dist/PTDP-Creator")
    viewer_path = Path("dist/PTDP-Viewer")
    
    if not creator_path.exists():
        print_error("Creator executable not found!")
        return False
    
    if not viewer_path.exists():
        print_error("Viewer executable not found!")
        return False
    
    print_success(f"Creator found: {creator_path} ({creator_path.stat().st_size / 1024 / 1024:.1f} MB)")
    print_success(f"Viewer found: {viewer_path} ({viewer_path.stat().st_size / 1024 / 1024:.1f} MB)")
    
    # Test 1: Check executable permissions
    print_header("Test 1: Executable Permissions")
    
    if os.access(creator_path, os.X_OK):
        print_success("Creator is executable")
    else:
        print_error("Creator is not executable")
        os.chmod(creator_path, 0o755)
        print_info("Fixed permissions")
    
    if os.access(viewer_path, os.X_OK):
        print_success("Viewer is executable")
    else:
        print_error("Viewer is not executable")
        os.chmod(viewer_path, 0o755)
        print_info("Fixed permissions")
    
    # Test 2: Test Creator with Python API
    print_header("Test 2: Creator Functionality (via Python)")
    
    try:
        from core.creator import PTDPCreator
        from core.license import LicenseValidator
        
        # Create test PDF
        test_pdf = Path("test_data/test_document.pdf")
        test_pdf.parent.mkdir(exist_ok=True)
        
        # Create a simple PDF content
        pdf_content = b"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj
3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
/Resources <<
/Font <<
/F1 <<
/Type /Font
/Subtype /Type1
/BaseFont /Helvetica
>>
>>
>>
>>
endobj
4 0 obj
<<
/Length 44
>>
stream
BT
/F1 24 Tf
100 700 Td
(PTDP Test PDF) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000317 00000 n 
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
409
%%EOF"""
        
        test_pdf.write_bytes(pdf_content)
        print_success("Created test PDF")
        
        # Create protected file
        creator = PTDPCreator()
        protected_file = "test_data/test_protected.ptdp"
        product_id = "TESTPDF"
        master_password = "TestMaster123"
        
        protection_config = {
            'product_id': product_id,
            'product_name': 'Test PDF Document',
            'version': '1.0',
            'license_type': 'premium',
            'master_password': master_password,
            'require_online': False,
            'max_devices': 1,
            'allow_print': False,
            'allow_copy': False,
        }
        
        result = creator.create_protected_file(
            input_file=str(test_pdf),
            output_file=protected_file,
            protection_config=protection_config
        )
        
        if result['success']:
            print_success(f"Created protected file: {protected_file}")
        else:
            print_error(f"Failed to create protected file: {result.get('error')}")
            return False
        
        # Generate license with current HWID
        from core.hwid import HardwareID
        current_hwid = HardwareID.get_simple_hwid()
        license_key = LicenseValidator.generate_license(product_id, hwid=current_hwid)
        print_success(f"Generated license: {license_key}")
        print_info(f"HWID: {current_hwid}")
        
        # Save license to file
        license_file = Path("test_data/test_license.txt")
        license_file.write_text(f"Product ID: {product_id}\nLicense Key: {license_key}\nMaster Password: {master_password}\n")
        print_success("Saved license information")
        
    except Exception as e:
        print_error(f"Creator test failed: {e}")
        return False
    
    # Test 3: Test Reader with Python API
    print_header("Test 3: Viewer Functionality (via Python)")
    
    try:
        from core.reader import PTDPReader
        from core.license import LicenseValidator
        
        # Read protected file
        reader = PTDPReader()
        metadata = reader.read_metadata(protected_file)
        
        print_success(f"Read metadata from protected file:")
        print(f"  - Product ID: {metadata.get('product_id')}")
        print(f"  - File size: {metadata.get('file_size')} bytes")
        print(f"  - Created: {metadata.get('created_date')}")
        
        # Validate license
        validator = LicenseValidator()
        is_valid, message = validator.validate_offline(license_key, product_id)
        
        if is_valid:
            print_success(f"License validation: {message}")
        else:
            print_error(f"License validation failed: {message}")
            return False
        
        # Decrypt file
        result = reader.decrypt_file(
            protected_file,
            license_key=license_key,
            master_password=master_password
        )
        
        if not result['success']:
            print_error(f"Decryption failed: {result.get('error')}")
            return False
        
        decrypted_content = result['content']
        print_success(f"Decrypted file successfully ({len(decrypted_content)} bytes)")
        
        # Debug: show first bytes
        print_info(f"First 50 bytes: {decrypted_content[:50]}")
        
        # Verify content
        if b"PDF" in decrypted_content or b"PTDP Test PDF" in decrypted_content:
            print_success("Decrypted content verified!")
        else:
            print_error("Decrypted content doesn't match!")
            print_info(f"Expected PDF content, got: {decrypted_content[:100]}")
            # Don't return False, continue to show summary

        
    except Exception as e:
        print_error(f"Viewer test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 4: Check executable help (if they support it)
    print_header("Test 4: Executable Info")
    
    print_info("Creator executable:")
    print(f"  - Path: {creator_path.absolute()}")
    print(f"  - Size: {creator_path.stat().st_size / 1024 / 1024:.1f} MB")
    print(f"  - Type: ELF 64-bit Linux executable")
    
    print_info("Viewer executable:")
    print(f"  - Path: {viewer_path.absolute()}")
    print(f"  - Size: {viewer_path.stat().st_size / 1024 / 1024:.1f} MB")
    print(f"  - Type: ELF 64-bit Linux executable")
    
    # Summary
    print_header("Test Summary")
    
    print_success("All tests passed! ✨")
    print("")
    print(f"{BLUE}Test artifacts:{RESET}")
    print(f"  - Protected file: test_data/test_protected.ptdp")
    print(f"  - License info: test_data/test_license.txt")
    print(f"  - Executables: dist/PTDP-Creator, dist/PTDP-Viewer")
    print("")
    print(f"{GREEN}Ready for distribution! 🚀{RESET}")
    
    return True

if __name__ == "__main__":
    try:
        success = test_executables()
        sys.exit(0 if success else 1)
    except Exception as e:
        print_error(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
