#!/usr/bin/env python3
"""
PTDP System Integration Test & Demo
Tests all components: creation, licensing, server, and decryption
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.creator import PTDPCreator
from core.reader import PTDPReader
from core.license import LicenseValidator
from core.hwid import HardwareID

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def test_complete_workflow():
    """Test complete workflow from protection to decryption"""
    
    print_header("PTDP COMPLETE WORKFLOW TEST")
    
    # Step 1: Create a test file
    print("\n📝 Step 1: Creating test file...")
    test_file = "test_document.txt"
    test_content = """
    ╔══════════════════════════════════════════════════════════╗
    ║          TEST DOCUMENT - PTDP PROTECTION DEMO           ║
    ╚══════════════════════════════════════════════════════════╝
    
    This is a test document to demonstrate PTDP protection.
    
    Features demonstrated:
    ✓ File encryption (AES-256)
    ✓ License validation
    ✓ Device locking
    ✓ Secure decryption
    
    If you can read this, the system works perfectly!
    
    © 2024 PTDP Protection System
    """
    
    with open(test_file, 'w') as f:
        f.write(test_content)
    print(f"✅ Created: {test_file}")
    
    # Step 2: Protect the file
    print("\n🔒 Step 2: Protecting file...")
    creator = PTDPCreator()
    
    protection_config = {
        'product_id': 'DEMO0001',
        'product_name': 'Demo Protected Document',
        'version': '1.0',
        'master_password': 'DemoPassword2024',
        'require_online': False,
        'max_devices': 1,
        'expiry_date': None,
        'view_limit': None
    }
    
    protected_file = 'test_document.ptdp'
    result = creator.create_protected_file(
        input_file=test_file,
        output_file=protected_file,
        protection_config=protection_config
    )
    
    if not result['success']:
        print(f"❌ Protection failed: {result.get('error')}")
        return False
    
    print(f"✅ Protected file created: {protected_file}")
    print(f"   Product ID: {result['product_id']}")
    print(f"   Size: {result['protected_size']} bytes")
    
    # Step 3: Generate license
    print("\n🔑 Step 3: Generating license key...")
    hwid = HardwareID.get_simple_hwid()
    
    license_key = LicenseValidator.generate_license(
        product_id='DEMO0001',
        hwid=hwid,
        expiry_date='LIFETIME'
    )
    
    print(f"✅ License generated: {license_key}")
    print(f"   Device ID: {hwid[:16]}...")
    
    # Step 4: Validate license (offline)
    print("\n✔️  Step 4: Validating license (offline)...")
    validator = LicenseValidator()
    valid, message = validator.validate_offline(license_key, 'DEMO0001')
    
    if valid:
        print(f"✅ License valid: {message}")
    else:
        print(f"❌ License invalid: {message}")
        return False
    
    # Step 5: Decrypt file
    print("\n🔓 Step 5: Decrypting file...")
    reader = PTDPReader()
    
    decrypted_file = 'test_document_decrypted.txt'
    decrypt_result = reader.decrypt_file(
        ptdp_file=protected_file,
        license_key=license_key,
        output_file=decrypted_file,
        master_password='DemoPassword2024'
    )
    
    if not decrypt_result['success']:
        print(f"❌ Decryption failed: {decrypt_result.get('error')}")
        return False
    
    print(f"✅ File decrypted successfully!")
    print(f"   Output: {decrypted_file}")
    
    # Step 6: Verify content
    print("\n✅ Step 6: Verifying decrypted content...")
    with open(test_file, 'r') as f:
        original = f.read()
    with open(decrypted_file, 'r') as f:
        decrypted = f.read()
    
    if original == decrypted:
        print("✅ Content matches perfectly!")
    else:
        print("❌ Content mismatch!")
        return False
    
    # Step 7: Test metadata reading
    print("\n📊 Step 7: Reading file metadata...")
    metadata = reader.read_metadata(protected_file)
    
    print(f"✅ Metadata retrieved:")
    print(f"   Product: {metadata['product_name']}")
    print(f"   Version: {metadata['version']}")
    print(f"   Created: {metadata['created_at']}")
    print(f"   Original size: {metadata['file_size']} bytes")
    print(f"   Encrypted size: {metadata['encrypted_size']} bytes")
    
    # Step 8: Test wrong license
    print("\n🚫 Step 8: Testing wrong license (should fail)...")
    wrong_license = "WRONG000-12345678-LIFETIME-ABCD1234"
    wrong_result = reader.decrypt_file(
        ptdp_file=protected_file,
        license_key=wrong_license,
        output_file='should_fail.txt',
        master_password='DemoPassword2024'
    )
    
    if not wrong_result['success']:
        print(f"✅ Correctly rejected: {wrong_result.get('error')}")
    else:
        print("❌ Security issue: Wrong license accepted!")
        return False
    
    # Cleanup
    print("\n🧹 Cleaning up test files...")
    for f in [test_file, protected_file, decrypted_file]:
        if os.path.exists(f):
            os.remove(f)
            print(f"   Removed: {f}")
    
    return True

def test_hwid_system():
    """Test hardware ID generation"""
    print_header("HARDWARE ID TEST")
    
    hwid = HardwareID.get_simple_hwid()
    info = HardwareID.get_system_info()
    
    print("\n🖥️  System Information:")
    for key, value in info.items():
        if key == 'hwid':
            print(f"   {key}: {value[:16]}... (truncated)")
        else:
            print(f"   {key}: {value}")
    
    print(f"\n✅ Hardware ID generated successfully")
    return True

def test_license_formats():
    """Test different license formats"""
    print_header("LICENSE FORMAT TESTS")
    
    test_cases = [
        ('PROD0001', None, 'LIFETIME', 'Any device, lifetime'),
        ('EBOOK001', 'ABC123XY', 'LIFETIME', 'Device locked, lifetime'),
        ('COURSE01', 'DEF456ZQ', '20251231', 'Device locked, expiry'),
    ]
    
    for product_id, hwid, expiry, desc in test_cases:
        print(f"\n📝 Test: {desc}")
        license_key = LicenseValidator.generate_license(
            product_id=product_id,
            hwid=hwid,
            expiry_date=expiry
        )
        print(f"   Product ID: {product_id}")
        print(f"   HWID: {hwid or 'ANY'}")
        print(f"   Expiry: {expiry}")
        print(f"   License: {license_key}")
    
    print(f"\n✅ All license formats generated successfully")
    return True

def main():
    """Run all tests"""
    print("="*70)
    print("  PTDP SYSTEM INTEGRATION TEST SUITE")
    print("  Testing all components end-to-end")
    print("="*70)
    
    tests = [
        ("Complete Workflow", test_complete_workflow),
        ("Hardware ID System", test_hwid_system),
        ("License Formats", test_license_formats),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test '{name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nTests Run: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print()
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {name}")
    
    if passed == total:
        print("\n" + "="*70)
        print("  🎉 ALL TESTS PASSED! SYSTEM READY FOR DEPLOYMENT")
        print("="*70)
        return 0
    else:
        print("\n" + "="*70)
        print("  ⚠️  SOME TESTS FAILED - REVIEW REQUIRED")
        print("="*70)
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
