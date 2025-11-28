# PTPD Viewer - User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Opening Protected Files](#opening-protected-files)
4. [Getting Your License Key](#getting-your-license-key)
5. [Troubleshooting](#troubleshooting)
6. [FAQ](#faq)

---

## Introduction

PTPD Viewer is an application that allows you to open and view protected digital products (.ptpd files). These files are encrypted and require a valid license key to access.

### What can be protected with PTPD?
- 📚 Ebooks (PDF, EPUB, MOBI)
- 📄 Documents (DOCX, XLSX, PPTX)
- 🎵 Audio files
- 🎬 Video files
- 💾 Software and data files
- And more!

---

## Installation

### Windows

1. **Download PTPD Viewer**
   - Download `PTPD-Viewer.exe` from your seller
   - Or from the official distribution site

2. **Install the Application**
   - Copy `PTPD-Viewer.exe` to a folder of your choice
   - Recommended: `C:\Program Files\PTPD Viewer\`

3. **Associate .ptpd Files (Optional)**
   - Right-click `register_ptpd.bat`
   - Select "Run as Administrator"
   - This allows double-clicking .ptpd files to open them

### macOS / Linux
Currently Windows only. macOS/Linux versions coming soon.

---

## Opening Protected Files

### Method 1: Using the Application

1. **Launch PTPD Viewer**
   - Double-click `PTPD-Viewer.exe`

2. **Open File**
   - Click "📂 Open PTPD File" button
   - Select your `.ptpd` file
   - File information will be displayed

3. **Enter License Key**
   - Type your license key in the text box
   - Format: `XXXX-XXXX-XXXX-XXXX`
   - Example: `EBOOK001-A1B2C3D4-LIFETIME-E5F6G7H8`

4. **Unlock File**
   - Click "🔓 Unlock & View File"
   - Wait for validation and decryption
   - File will open in its default application

### Method 2: Double-Click (if registered)

1. Double-click any `.ptpd` file
2. PTPD Viewer opens automatically
3. Enter your license key
4. Click unlock

---

## Getting Your License Key

### Where to Get It
License keys are provided by the seller when you purchase a protected product.

### License Key Format
```
PRODUCT-DEVICE-EXPIRY-SIGNATURE
  │       │      │        │
  │       │      │        └─ Cryptographic signature
  │       │      └────────── Expiry date or "LIFETIME"
  │       └───────────────── Device ID (if device-locked)
  └───────────────────────── Product identifier
```

### Example License Keys

**Lifetime License (Any Device):**
```
EBOOK001-ANYDEVIC-LIFETIME-A1B2C3D4
```

**Device-Locked License:**
```
EBOOK001-12345678-LIFETIME-E5F6G7H8
```

**Time-Limited License:**
```
EBOOK001-ANYDEVIC-20251231-K9L0M1N2
```

---

## Your Device ID

### What is it?
Your Device ID is a unique identifier for your computer. Some licenses are locked to specific devices for security.

### How to Find It
1. Open PTPD Viewer
2. Look at the bottom of the window
3. You'll see: "🖥️ Your Device ID: XXXXXXXX..."
4. Click it to copy to clipboard

### When You Need It
- When requesting a device-locked license from a seller
- When troubleshooting license issues
- When contacting support

---

## Troubleshooting

### "Invalid PTPD file format"

**Problem:** File is corrupted or not a valid .ptpd file

**Solutions:**
- Re-download the file
- Check file size (should not be 0 KB)
- Verify you downloaded the complete file
- Contact the seller for a new copy

---

### "License validation failed"

**Problem:** License key is incorrect or invalid

**Solutions:**
- Double-check your license key (copy-paste to avoid typos)
- Verify you're using the correct license for this product
- Check if license has expired
- Contact seller to verify license status

---

### "Device mismatch"

**Problem:** License is locked to a different device

**Solutions:**
- This license is for another computer
- Contact seller with YOUR Device ID for a new license
- If you changed hardware, you may need a new license

---

### "License expired"

**Problem:** Your license has passed its expiry date

**Solutions:**
- Contact seller for license renewal
- Purchase extended license
- Check if lifetime licenses are available

---

### "View limit reached"

**Problem:** You've opened the file the maximum allowed times

**Solutions:**
- Some products have view limits (e.g., 10 views)
- Contact seller to reset or purchase unlimited views
- Check product terms for view limits

---

### "No internet connection" (Online Validation)

**Problem:** Some licenses require internet to validate

**Solutions:**
- Connect to the internet
- Check your firewall settings
- If offline mode is available, it will work automatically
- Contact seller for offline license

---

### File won't open after unlocking

**Problem:** Decrypted file doesn't open

**Solutions:**
- Install the required application for the file type
- For PDFs: Install Adobe Reader or similar
- For videos: Install VLC or similar
- File may open in background - check taskbar

---

## FAQ

### Q: Is PTPD Viewer free?
**A:** Yes, PTPD Viewer is free. You only pay for the protected content, not the viewer.

### Q: Can I share my license key?
**A:** No. Each license is for one buyer. Sharing violates terms and may result in license deactivation.

### Q: Can I use one license on multiple computers?
**A:** Depends on the license type. Check with the seller:
- Single device: Only one computer
- Multi-device: Up to N computers
- Device-locked: Specific computer only

### Q: What happens to the decrypted file?
**A:** The file opens temporarily and is automatically deleted when closed. Your .ptpd file remains protected.

### Q: Can I convert .ptpd files back to normal files?
**A:** No. Once decrypted, files are temporary. You always need the .ptpd and license to access content.

### Q: Is my data safe?
**A:** Yes. PTPD uses AES-256 encryption (military grade). Your files and license keys are secure.

### Q: Can I get a refund if license doesn't work?
**A:** Contact the seller directly. Refund policies vary by seller.

### Q: How long do licenses last?
**A:** Depends on the license type:
- Lifetime: Forever
- Time-limited: Until expiry date
- View-limited: Until views exhausted

### Q: Can I backup my .ptpd files?
**A:** Yes! Keep backups of your .ptpd files and license keys in a safe place.

---

## Support

### For License Issues
Contact the product seller with:
- Your license key
- Your Device ID
- Product name
- Error message screenshot

### For Technical Issues
1. Check this guide first
2. Try restarting PTPD Viewer
3. Re-download the .ptpd file
4. Contact seller if issue persists

### For Feature Requests
Email: support@example.com (replace with actual support email)

---

## Tips for Best Experience

✅ **DO:**
- Keep license keys in a safe place (password manager recommended)
- Backup your .ptpd files
- Update PTPD Viewer when new versions are available
- Close the application properly after use

❌ **DON'T:**
- Share license keys with others
- Try to modify .ptpd files
- Use license key generators (they don't work and may be malware)
- Distribute protected content without permission

---

© 2024 PTPD Protection System
