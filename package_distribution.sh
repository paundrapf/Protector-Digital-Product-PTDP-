#!/bin/bash
# Package PTDP executables for distribution

echo "📦 Creating PTDP Distribution Package"
echo "======================================"
echo ""

# Create distribution directory
DIST_DIR="ptdp_distribution"
mkdir -p "$DIST_DIR"

# Create subdirectories
mkdir -p "$DIST_DIR/for_sellers"
mkdir -p "$DIST_DIR/for_users"
mkdir -p "$DIST_DIR/samples"

echo "✓ Created distribution structure"

# Copy executables
cp dist/PTDP-Creator "$DIST_DIR/for_sellers/"
cp dist/PTDP-Viewer "$DIST_DIR/for_users/"

echo "✓ Copied executables"

# Copy sample files
if [ -d "samples/protected" ]; then
    cp samples/protected/*.ptdp "$DIST_DIR/samples/" 2>/dev/null || true
fi

if [ -d "test_data" ]; then
    cp test_data/test_protected.ptdp "$DIST_DIR/samples/sample.ptdp" 2>/dev/null || true
    cp test_data/test_license.txt "$DIST_DIR/samples/sample_license.txt" 2>/dev/null || true
fi

echo "✓ Copied sample files"

# Create README for sellers
cat > "$DIST_DIR/for_sellers/README.txt" << 'EOF'
🔐 PTDP Creator - For Sellers & Content Creators
=================================================

What is this?
-------------
PTDP Creator allows you to protect your PDF files with military-grade 
encryption. Perfect for selling eBooks, courses, documents, and other 
digital products.

How to use:
-----------
1. Run PTDP-Creator executable
2. Select your PDF file
3. Configure protection settings:
   - Product ID (e.g., "EBOOK001")
   - Master password (keep this secret!)
   - License settings
4. Click "Protect File"
5. Share the .ptdp file with customers
6. Generate license keys for each customer

Features:
---------
✅ AES-256 encryption
✅ Hardware ID (HWID) locking
✅ License key system
✅ Expiry date support
✅ PDF-only protection

Support:
--------
For issues or questions, check the documentation in the main folder.

License:
--------
Commercial use allowed. See LICENSE file for details.
EOF

# Create README for users
cat > "$DIST_DIR/for_users/README.txt" << 'EOF'
📖 PTDP Viewer - For End Users
================================

What is this?
-------------
PTDP Viewer allows you to open and read protected PDF files (.ptdp).
If you received a .ptdp file, this is the app you need!

How to use:
-----------
1. Run PTDP-Viewer executable
2. Click "Open Protected File"
3. Select your .ptdp file
4. Enter your license key (provided by the seller)
5. View your PDF content
6. Export to regular PDF if needed

Requirements:
-------------
- Valid license key from the seller
- Internet connection (for online validation)
- The device HWID may be locked to your machine

Features:
---------
✅ Secure PDF viewing
✅ License validation
✅ Export to PDF
✅ Modern, clean interface

Support:
--------
If you have issues with your license key, contact the seller who 
provided the .ptdp file.

License:
--------
Free to use. See LICENSE file for details.
EOF

# Create main README
cat > "$DIST_DIR/README.txt" << 'EOF'
🚀 PTDP - Protector Digital Product
====================================

Version: 2.0
Build Date: $(date +%Y-%m-%d)

Contents:
---------
📁 for_sellers/    - PTDP Creator (protect your PDFs)
📁 for_users/      - PTDP Viewer (open protected PDFs)
📁 samples/        - Sample protected files

Quick Links:
------------
🌐 Website: [Your website here]
📖 Documentation: See docs folder
💬 Support: [Your support email]

What's New in v2.0:
-------------------
✨ Gen-Z styled interface
✨ PDF-only focus
✨ Modern CustomTkinter GUI
✨ Improved security
✨ Better performance

System Requirements:
--------------------
- Linux (64-bit)
- 100MB disk space
- Internet connection (recommended)

Getting Started:
----------------
👉 Sellers: Open for_sellers/README.txt
👉 Users: Open for_users/README.txt

License:
--------
See LICENSE file for terms and conditions.

---
Built with 💖 for digital product creators
EOF

echo "✓ Created README files"

# Create license file
cat > "$DIST_DIR/LICENSE.txt" << 'EOF'
PTDP License Agreement
======================

Copyright (c) 2025 PTDP Project

Permission is hereby granted to use this software for commercial 
and personal purposes.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.

For full license details, see the LICENSE file in the source repository.
EOF

echo "✓ Created license file"

# Create version info
cat > "$DIST_DIR/VERSION.txt" << EOF
PTDP Version 2.0
Build Date: $(date +%Y-%m-%d)
Build Time: $(date +%H:%M:%S)

Executables:
- PTDP-Creator: $(ls -lh dist/PTDP-Creator | awk '{print $5}')
- PTDP-Viewer: $(ls -lh dist/PTDP-Viewer | awk '{print $5}')

Components:
- Python: 3.12.1
- Cryptography: AES-256
- License System: HWID-locked
- File Format: .ptdp

Gen-Z Edition Features:
- Modern UI/UX
- PDF-only protection
- Enhanced security
- Smooth animations
EOF

echo "✓ Created version info"

# Create archive
echo ""
echo "Creating archive..."
tar -czf ptdp_v2.0_linux_x64.tar.gz "$DIST_DIR"

echo ""
echo "======================================"
echo "✅ Distribution package ready!"
echo ""
echo "📁 Directory: $DIST_DIR/"
echo "📦 Archive: ptdp_v2.0_linux_x64.tar.gz"
echo ""
echo "File sizes:"
ls -lh ptdp_v2.0_linux_x64.tar.gz
echo ""
echo "Contents:"
tree -L 2 "$DIST_DIR" 2>/dev/null || ls -R "$DIST_DIR"
echo ""
echo "🚀 Ready for distribution!"
