#!/usr/bin/env python3
"""
Quick manual test of sample files
"""

from core.reader import PTDPReader
from core.license import LicenseValidator

# Test with trading ebook
print("🧪 Testing trading_ebook.ptdp")
print("=" * 50)

reader = PTDPReader()
protected_file = "samples/protected/trading_ebook.ptdp"
# Use license for current device
license_key = "EBOOK001-3F1AA252-LIFETIME-D9C8B1C5"
master_password = "EbookSecret2024"

# Read metadata
print("\n📋 Metadata:")
metadata = reader.read_metadata(protected_file)
for key, value in metadata.items():
    print(f"  {key}: {value}")

# Validate license
print("\n🔐 License Validation:")
validator = LicenseValidator()
is_valid, message = validator.validate_offline(license_key, "EBOOK001")
print(f"  Status: {'✅ VALID' if is_valid else '❌ INVALID'}")
print(f"  Message: {message}")

# Decrypt
print("\n🔓 Decryption:")
result = reader.decrypt_file(
    protected_file,
    license_key=license_key,
    master_password=master_password
)

if result['success']:
    content = result['content']
    print(f"  ✅ Success! Decrypted {len(content)} bytes")
    print(f"  First 100 bytes: {content[:100]}")
    
    # Save to file
    with open("test_decrypted.pdf", "wb") as f:
        f.write(content)
    print(f"  💾 Saved to: test_decrypted.pdf")
else:
    print(f"  ❌ Failed: {result.get('error')}")

print("\n" + "=" * 50)
print("✅ Manual test completed!")
