# PTPD Protection System - Developer Guide

## For Sellers, Content Creators, and Developers

---

## Table of Contents

1. [Overview](#overview)
2. [Installation & Setup](#installation--setup)
3. [Protecting Your First Product](#protecting-your-first-product)
4. [License Management](#license-management)
5. [Distribution Workflow](#distribution-workflow)
6. [Server Setup](#server-setup)
7. [Advanced Features](#advanced-features)
8. [API Reference](#api-reference)
9. [Best Practices](#best-practices)

---

## Overview

PTPD is a complete digital product protection system that includes:
- **File Encryption**: AES-256 encryption for maximum security
- **License Management**: Flexible licensing with device locks, expiry dates
- **Hardware Locking**: Tie licenses to specific devices
- **Online/Offline Validation**: Support for both modes
- **View Limiting**: Control how many times files can be opened

---

## Installation & Setup

### Prerequisites
```bash
Python 3.8+
pip (Python package manager)
```

### Install Dependencies
```bash
cd ptpd-protection
pip install -r requirements.txt
```

### Verify Installation
```bash
python -c "from core import PTPDCreator; print('✅ Installation successful!')"
```

---

## Protecting Your First Product

### Method 1: Using GUI (Easiest)

1. **Run PTPD Creator**
   ```bash
   python gui/creator.py
   ```

2. **Fill in Details**
   - Select file to protect
   - Enter Product ID (e.g., `EBOOK001`)
   - Enter Product Name
   - Set master password (KEEP THIS SECRET!)
   - Configure options

3. **Create Protected File**
   - Click "Create Protected File"
   - Save the `.ptpd` file
   - **IMPORTANT**: Save master password and Product ID!

### Method 2: Using Python Code

```python
from core.creator import PTPDCreator

creator = PTPDCreator()

# Configure protection
config = {
    'product_id': 'EBOOK001',
    'product_name': 'Advanced Trading Guide',
    'master_password': 'SuperSecret123!',  # KEEP SECRET!
    'require_online': False,
    'max_devices': 1,
    'expiry_date': None,  # Lifetime
    'view_limit': None,   # Unlimited
}

# Protect file
result = creator.create_protected_file(
    input_file='my_ebook.pdf',
    output_file='my_ebook.ptpd',
    config=config
)

if result['success']:
    print(f"✅ Protected: {result['output_file']}")
    print(f"🆔 Product ID: {result['product_id']}")
```

### Method 3: Command Line

```bash
python core/creator.py
```

Follow the prompts.

---

## License Management

### Getting Buyer's Device ID

Buyers can find their Device ID in PTPD Viewer (bottom of window). They should send this to you.

### Generating License Keys

#### Any Device License (Less Secure)
```python
from core.license import LicenseValidator

license = LicenseValidator.generate_license(
    product_id='EBOOK001',
    hwid=None,  # Any device
    expiry_date='LIFETIME'
)

print(f"License: {license}")
# Send this to buyer
```

#### Device-Locked License (Recommended)
```python
license = LicenseValidator.generate_license(
    product_id='EBOOK001',
    hwid=buyer_device_id,  # Specific device
    expiry_date='LIFETIME'
)
```

#### Time-Limited License
```python
license = LicenseValidator.generate_license(
    product_id='EBOOK001',
    hwid=buyer_device_id,
    expiry_date='20251231'  # Format: YYYYMMDD
)
```

### CLI Tool for License Generation

```bash
python core/license.py
```

Interactive prompts will guide you.

---

## Distribution Workflow

### Recommended Workflow

```
1. CREATE PRODUCT
   ├─ Protect file with PTPD Creator
   ├─ Save master password securely
   └─ Upload .ptpd file to distribution platform

2. BUYER PURCHASES
   ├─ Buyer downloads .ptpd file
   ├─ Buyer downloads PTPD Viewer (if needed)
   └─ Buyer sends you their Device ID

3. GENERATE LICENSE
   ├─ Generate device-locked license
   └─ Send license key to buyer via email

4. BUYER USES PRODUCT
   ├─ Opens .ptpd file in PTPD Viewer
   ├─ Enters license key
   └─ Enjoys the protected content
```

### Distribution Platforms

Upload your `.ptpd` files to:
- **Your website**: Direct downloads
- **Gumroad**: Digital product marketplace
- **Google Drive**: With purchase verification
- **Your own server**: With automated delivery
- **Membership sites**: Protected downloads

---

## Server Setup

### Why Run a Server?

- **Online license validation**: Real-time verification
- **License management**: Activate/deactivate remotely
- **Usage tracking**: Monitor license usage
- **Multi-device control**: Manage device limits

### Quick Start

1. **Start the server**
   ```bash
   cd server
   python api.py
   ```

2. **Server runs on** `http://localhost:5000`

3. **Update config.py**
   ```python
   API_URL = "http://your-server.com/api"
   ```

### Production Deployment

#### Using Heroku (Free Tier)

```bash
# Install Heroku CLI
heroku login
heroku create ptpd-license-server
git push heroku main
```

#### Using DigitalOcean

```bash
# Create droplet
# SSH into server
git clone your-repo
cd ptpd-protection/server
pip install -r ../requirements.txt
python api.py
```

#### Using Docker

```dockerfile
# Dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "server/api.py"]
```

### API Endpoints

**Validate License**
```http
POST /api/validate
Content-Type: application/json

{
  "license_key": "EBOOK001-...",
  "product_id": "EBOOK001",
  "hwid": "abc123..."
}
```

**Generate License** (Admin)
```http
POST /api/generate
X-API-Key: YOUR_SECRET_KEY
Content-Type: application/json

{
  "product_id": "EBOOK001",
  "hwid": "abc123...",
  "expiry": "2025-12-31",
  "max_devices": 1
}
```

---

## Advanced Features

### Batch Protection

Protect multiple files at once:

```python
from core.creator import PTPDCreator

creator = PTPDCreator()

files = [
    'chapter1.pdf',
    'chapter2.pdf',
    'chapter3.pdf'
]

config_template = {
    'master_password': 'MySecret123',
    'license_type': 'premium',
    'max_devices': 1
}

result = creator.batch_protect(
    input_files=files,
    output_dir='protected_output',
    config_template=config_template
)

print(f"Protected: {result['success']}/{result['total']}")
```

### Watermarking

Add buyer info to files:

```python
config = {
    'product_id': 'EBOOK001',
    'product_name': 'My Ebook',
    'master_password': 'secret',
    'watermark': 'Licensed to: {buyer_email}'
}
```

### View Limiting

Limit how many times files can be opened:

```python
config = {
    'product_id': 'EBOOK001',
    'product_name': 'Trial Version',
    'master_password': 'secret',
    'view_limit': 10  # Can only open 10 times
}
```

---

## API Reference

### PTPDCreator

```python
class PTPDCreator:
    def create_protected_file(input_file, output_file, config):
        """
        Protect a file
        
        Args:
            input_file (str): Path to file to protect
            output_file (str): Path to save .ptpd file
            config (dict): Protection configuration
            
        Returns:
            dict: {'success': bool, 'output_file': str, ...}
        """
```

### PTPDReader

```python
class PTPDReader:
    def decrypt_file(ptpd_file, license_key, output_file=None):
        """
        Decrypt protected file
        
        Args:
            ptpd_file (str): Path to .ptpd file
            license_key (str): Valid license key
            output_file (str): Optional output path
            
        Returns:
            dict: {'success': bool, 'content': bytes, ...}
        """
    
    def read_metadata(ptpd_file):
        """Get file metadata without decrypting"""
```

### LicenseValidator

```python
class LicenseValidator:
    @staticmethod
    def generate_license(product_id, hwid=None, expiry_date='LIFETIME'):
        """
        Generate license key
        
        Args:
            product_id (str): Product identifier
            hwid (str): Device ID or None for any device
            expiry_date (str): 'LIFETIME' or 'YYYYMMDD'
            
        Returns:
            str: License key
        """
    
    def validate_online(license_key, product_id):
        """Validate with server"""
    
    def validate_offline(license_key, product_id):
        """Validate without server"""
```

---

## Best Practices

### Security

✅ **DO:**
- Keep master passwords in a password manager
- Use device-locked licenses when possible
- Enable online validation for high-value products
- Rotate SECRET_KEY in config.py
- Use HTTPS for server deployment

❌ **DON'T:**
- Hardcode master passwords in scripts
- Share master passwords with anyone
- Use weak passwords (min 12 chars recommended)
- Commit secrets to version control

### License Strategy

**For Digital Products:**
- Use device-locked licenses
- Set reasonable expiry dates
- Consider multi-device licenses for families

**For Trials:**
- Use view limits (e.g., 3 views)
- Set short expiry dates (e.g., 7 days)
- Offer easy upgrade path

**For Enterprise:**
- Use online validation
- Set device limits (e.g., 100 devices)
- Provide admin dashboard

### Customer Support

Collect from buyers when they have issues:
1. License key
2. Device ID
3. Error message screenshot
4. Product name

Common issues:
- Wrong license key format (teach copy-paste)
- Device mismatch (need new license)
- Expired license (offer renewal)

---

## Building Executables

### Build Tools

```bash
python build.py
```

This creates:
- `dist/PTPD-Viewer.exe` - For end-users
- `dist/PTPD-Creator.exe` - For you

### Distribute to Users

1. Package `PTPD-Viewer.exe` with:
   - `README.txt` (user guide)
   - `register_ptpd.bat` (optional)

2. Upload to your website or distribution platform

3. Provide download link to buyers

---

## Troubleshooting

### Build Fails

```bash
# Install/upgrade PyInstaller
pip install --upgrade pyinstaller

# Clean build
python build.py --clean
```

### License Not Validating

Check:
1. SECRET_KEY in config.py matches
2. Product ID format (max 8 chars)
3. HWID is correct
4. Date format is YYYYMMDD

### Server Not Starting

```bash
# Check port 5000 is free
netstat -an | grep 5000

# Try different port
app.run(port=5001)
```

---

## Example Projects

See `example_usage.py` for complete working examples:

```bash
python example_usage.py
```

---

## Support & Community

- **GitHub**: [Link to repo]
- **Email**: support@example.com
- **Discord**: [Link to server]

---

© 2024 PTPD Protection System - Developer Guide
