# core/license.py
"""
License Management Module
Generate, validate, and manage product licenses
"""

import requests
import json
import hashlib
from datetime import datetime
from .hwid import HardwareID
import sys
import os

# Import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class LicenseValidator:
    """License validation dan generation"""
    
    def __init__(self, api_url=None):
        self.api_url = api_url or config.API_URL
        self.hwid = HardwareID.get_simple_hwid()
        self.secret_key = config.SECRET_KEY
    
    def validate_online(self, license_key, product_id):
        """
        Validasi license ke server online
        
        Returns:
            tuple: (valid: bool, message: str)
        """
        try:
            response = requests.post(
                f"{self.api_url}/validate",
                json={
                    'license_key': license_key,
                    'product_id': product_id,
                    'hwid': self.hwid
                },
                timeout=config.API_TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                return data['valid'], data.get('message', '')
            else:
                return False, f"Server error: {response.status_code}"
        
        except requests.exceptions.Timeout:
            print("⚠️  Server timeout, trying offline validation...")
            return self.validate_offline(license_key, product_id)
        
        except requests.exceptions.ConnectionError:
            print("⚠️  No internet connection, trying offline validation...")
            return self.validate_offline(license_key, product_id)
        
        except Exception as e:
            print(f"⚠️  Online validation error: {e}")
            return self.validate_offline(license_key, product_id)
    
    def validate_offline(self, license_key, product_id):
        """
        Validasi offline dengan cryptographic signature
        Format: PRODUCT-HWID-EXPIRY-SIGNATURE
        
        Returns:
            tuple: (valid: bool, message: str)
        """
        try:
            # Parse license key
            parts = license_key.split('-')
            if len(parts) < 4:
                return False, "Invalid license format (expected XXXX-XXXX-XXXX-XXXX)"
            
            stored_product = parts[0]
            stored_hwid = parts[1]
            expiry_date = parts[2]
            signature = parts[3]
            
            # Validate product ID
            product_short = product_id[:8].upper().replace('-', '').replace('_', '')
            if stored_product != product_short:
                return False, f"Invalid product (expected {product_short}, got {stored_product})"
            
            # Validate HWID (device lock)
            if config.ENABLE_HWID_LOCK:
                hwid_short = self.hwid[:8].upper()
                if stored_hwid != hwid_short:
                    return False, f"License locked to different device (HWID: {stored_hwid})"
            
            # Validate expiry
            if expiry_date != "LIFETIME":
                try:
                    exp_date = datetime.strptime(expiry_date, "%Y%m%d")
                    if datetime.now() > exp_date:
                        return False, f"License expired on {exp_date.strftime('%Y-%m-%d')}"
                except ValueError:
                    return False, "Invalid expiry date format"
            
            # Verify cryptographic signature
            verify_string = f"{stored_product}{stored_hwid}{expiry_date}{self.secret_key}"
            verify_hash = hashlib.sha256(verify_string.encode()).hexdigest()[:8].upper()
            
            if verify_hash != signature:
                return False, "Invalid license signature (tampered or fake)"
            
            # All checks passed
            expiry_msg = "LIFETIME" if expiry_date == "LIFETIME" else expiry_date
            return True, f"Valid license (expires: {expiry_msg})"
        
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    @staticmethod
    def generate_license(product_id, hwid=None, expiry_date="LIFETIME"):
        """
        Generate license key - untuk admin/seller
        
        Args:
            product_id: Product identifier (e.g., "EBOOK001")
            hwid: Hardware ID (None = any device, specific ID = locked)
            expiry_date: "LIFETIME" atau "YYYYMMDD" format
        
        Returns:
            str: License key format PRODUCT-HWID-EXPIRY-SIGNATURE
        """
        # Get HWID
        if hwid is None:
            hwid = "ANYDEVIC"  # Allow any device
        
        # Normalize product ID (8 chars)
        product_short = product_id[:8].upper().replace('-', '').replace('_', '')
        product_short = product_short.ljust(8, '0')  # Pad if shorter
        
        # Normalize HWID (8 chars)
        if hwid == "ANYDEVIC":
            hwid_short = "ANYDEVIC"
        else:
            hwid_short = hwid[:8].upper()
        
        # Normalize expiry
        if expiry_date and expiry_date != "LIFETIME":
            # Validate date format
            try:
                datetime.strptime(expiry_date, "%Y%m%d")
            except ValueError:
                expiry_date = "LIFETIME"
        
        # Generate signature
        secret = config.SECRET_KEY
        signature_string = f"{product_short}{hwid_short}{expiry_date}{secret}"
        signature = hashlib.sha256(signature_string.encode()).hexdigest()[:8].upper()
        
        # Construct license key
        license_key = f"{product_short}-{hwid_short}-{expiry_date}-{signature}"
        
        return license_key
    
    @staticmethod
    def parse_license(license_key):
        """
        Parse license key untuk mendapatkan info
        
        Returns:
            dict: License information
        """
        try:
            parts = license_key.split('-')
            if len(parts) >= 4:
                return {
                    'product_id': parts[0],
                    'hwid': parts[1],
                    'expiry': parts[2],
                    'signature': parts[3],
                    'valid_format': True
                }
            return {'valid_format': False}
        except:
            return {'valid_format': False}

# ========================
# CLI Tools
# ========================

def generate_license_cli():
    """Command-line tool untuk generate license"""
    print("🔑 PTPD License Generator")
    print("=" * 50)
    
    product_id = input("Product ID (e.g., EBOOK001): ").strip()
    
    print("\nDevice Lock:")
    print("  1. Lock to specific device (enter HWID)")
    print("  2. Any device (no lock)")
    choice = input("Choice [1/2]: ").strip()
    
    if choice == "1":
        hwid = input("Enter buyer's HWID: ").strip()
    else:
        hwid = None
    
    print("\nExpiry:")
    print("  1. Lifetime")
    print("  2. Specific date (YYYYMMDD)")
    choice = input("Choice [1/2]: ").strip()
    
    if choice == "2":
        expiry = input("Enter date (YYYYMMDD): ").strip()
    else:
        expiry = "LIFETIME"
    
    # Generate
    license_key = LicenseValidator.generate_license(
        product_id=product_id,
        hwid=hwid,
        expiry_date=expiry
    )
    
    print("\n" + "=" * 50)
    print(f"✅ License Generated:")
    print(f"\n{license_key}\n")
    print("=" * 50)
    
    # Parse and show info
    info = LicenseValidator.parse_license(license_key)
    print(f"\nProduct ID: {info['product_id']}")
    print(f"Device Lock: {info['hwid']}")
    print(f"Expiry: {info['expiry']}")

if __name__ == "__main__":
    # Run CLI tool
    generate_license_cli()
