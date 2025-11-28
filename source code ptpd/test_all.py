#!/usr/bin/env python3
"""
Test Suite untuk PTPD Protection System
Run: python tests/test_all.py
"""

import unittest
import os
import sys
import tempfile

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.creator import PTPDCreator
from core.reader import PTPDReader
from core.license import LicenseValidator
from core.hwid import HardwareID

class TestHWID(unittest.TestCase):
    def test_hwid_generation(self):
        """Test HWID generation"""
        hwid1 = HardwareID.get_simple_hwid()
        hwid2 = HardwareID.get_simple_hwid()
        
        self.assertIsNotNone(hwid1)
        self.assertEqual(hwid1, hwid2)  # Should be consistent
        self.assertEqual(len(hwid1), 32)  # Should be 32 chars

class TestLicense(unittest.TestCase):
    def test_license_generation(self):
        """Test license key generation"""
        license = LicenseValidator.generate_license(
            product_id='TEST001',
            hwid='12345678',
            expiry_date='LIFETIME'
        )
        
        self.assertIsNotNone(license)
        self.assertIn('-', license)
        parts = license.split('-')
        self.assertEqual(len(parts), 4)
    
    def test_license_validation_offline(self):
        """Test offline license validation"""
        validator = LicenseValidator()
        hwid = HardwareID.get_simple_hwid()
        
        # Generate valid license
        license = LicenseValidator.generate_license(
            product_id='TEST001',
            hwid=hwid,
            expiry_date='LIFETIME'
        )
        
        # Validate
        valid, message = validator.validate_offline(license, 'TEST001')
        self.assertTrue(valid, f"Validation failed: {message}")
    
    def test_invalid_license(self):
        """Test invalid license rejection"""
        validator = LicenseValidator()
        
        valid, message = validator.validate_offline(
            'INVALID-LICENSE-KEY',
            'TEST001'
        )
        
        self.assertFalse(valid)

class TestProtection(unittest.TestCase):
    def setUp(self):
        """Setup test files"""
        self.test_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        self.test_file.write("This is test content for PTPD protection system.\n" * 100)
        self.test_file.close()
        
        self.ptpd_file = self.test_file.name.replace('.txt', '.ptpd')
        self.output_file = self.test_file.name.replace('.txt', '_decrypted.txt')
    
    def tearDown(self):
        """Cleanup test files"""
        for f in [self.test_file.name, self.ptpd_file, self.output_file]:
            if os.path.exists(f):
                os.remove(f)
    
    def test_file_protection(self):
        """Test file protection"""
        creator = PTPDCreator()
        
        config = {
            'product_id': 'TEST001',
            'product_name': 'Test Product',
            'master_password': 'TestPassword123',
            'require_online': False,
            'max_devices': 1
        }
        
        result = creator.create_protected_file(
            self.test_file.name,
            self.ptpd_file,
            config
        )
        
        self.assertTrue(result['success'], f"Protection failed: {result.get('error')}")
        self.assertTrue(os.path.exists(self.ptpd_file))
    
    def test_file_decryption(self):
        """Test file decryption"""
        # First protect
        creator = PTPDCreator()
        config = {
            'product_id': 'TEST001',
            'product_name': 'Test Product',
            'master_password': 'TestPassword123',
            'require_online': False,
            'max_devices': 1
        }
        
        result = creator.create_protected_file(
            self.test_file.name,
            self.ptpd_file,
            config
        )
        
        self.assertTrue(result['success'])
        
        # Generate license
        hwid = HardwareID.get_simple_hwid()
        license = LicenseValidator.generate_license(
            product_id='TEST001',
            hwid=hwid,
            expiry_date='LIFETIME'
        )
        
        # Decrypt
        reader = PTPDReader()
        result = reader.decrypt_file(
            self.ptpd_file,
            license,
            self.output_file
        )
        
        self.assertTrue(result['success'], f"Decryption failed: {result.get('error')}")
        self.assertTrue(os.path.exists(self.output_file))
        
        # Verify content
        with open(self.test_file.name, 'r') as f:
            original = f.read()
        with open(self.output_file, 'r') as f:
            decrypted = f.read()
        
        self.assertEqual(original, decrypted)
    
    def test_wrong_license(self):
        """Test wrong license rejection"""
        # Protect file
        creator = PTPDCreator()
        config = {
            'product_id': 'TEST001',
            'product_name': 'Test Product',
            'master_password': 'TestPassword123',
            'require_online': False,
            'max_devices': 1
        }
        
        creator.create_protected_file(
            self.test_file.name,
            self.ptpd_file,
            config
        )
        
        # Try wrong license
        reader = PTPDReader()
        result = reader.decrypt_file(
            self.ptpd_file,
            'WRONG-LICENSE-KEY-HERE',
            self.output_file
        )
        
        self.assertFalse(result['success'])
    
    def test_metadata_reading(self):
        """Test metadata reading"""
        # Protect file
        creator = PTPDCreator()
        config = {
            'product_id': 'TEST001',
            'product_name': 'Test Product',
            'master_password': 'TestPassword123',
            'require_online': False,
            'max_devices': 1
        }
        
        creator.create_protected_file(
            self.test_file.name,
            self.ptpd_file,
            config
        )
        
        # Read metadata
        reader = PTPDReader()
        metadata = reader.read_metadata(self.ptpd_file)
        
        self.assertEqual(metadata['product_id'], 'TEST001')
        self.assertEqual(metadata['product_name'], 'Test Product')
        self.assertEqual(metadata['max_devices'], 1)

def run_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("PTPD Protection System - Test Suite")
    print("="*60 + "\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add tests
    suite.addTests(loader.loadTestsFromTestCase(TestHWID))
    suite.addTests(loader.loadTestsFromTestCase(TestLicense))
    suite.addTests(loader.loadTestsFromTestCase(TestProtection))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "="*60)
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED")
        print(f"   Failures: {len(result.failures)}")
        print(f"   Errors: {len(result.errors)}")
    print("="*60 + "\n")
    
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests())
