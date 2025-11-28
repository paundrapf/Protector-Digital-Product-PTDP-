# 🔒 PTDP Protection System
## Protected Digital Product Format

**Sistem proteksi file digital dengan enkripsi AES-256, license validation, dan hardware lock**

---

## 📦 Tentang PTDP

**PTDP (Protected Digital Product)** adalah format file custom `.ptdp` yang dirancang untuk melindungi produk digital seperti ebook, course, template, dan konten premium lainnya dengan enkripsi tingkat enterprise.

### ✨ Fitur Utama

- 🔐 **Enkripsi AES-256** - Military-grade encryption
- 🔑 **License Management** - Offline/online validation
- 💻 **Hardware Locking** - Bind license ke device tertentu  
- ⏰ **Expiry Date** - Set tanggal kadaluarsa
- 👁️ **View Limit** - Batasi jumlah views
- 📊 **Usage Tracking** - Monitor penggunaan
- 🌐 **Multi-Platform** - Windows, macOS, Linux support
- 🎨 **Modern UI** - Beautiful dark theme GUI

---

## 📁 Struktur Project

```
PTDP-Protection/
├── core/                    # Core modules
│   ├── __init__.py
│   ├── creator.py          # File protection/encryption
│   ├── reader.py           # File decryption/reading
│   ├── license.py          # License management
│   └── hwid.py             # Hardware ID detection
├── gui/                     # GUI applications
│   ├── __init__.py
│   ├── viewer.py           # End-user viewer app
│   └── creator.py          # Admin creator tool
├── server/                  # License server
│   ├── __init__.py
│   └── api.py              # Flask REST API
├── tests/                   # Unit tests
│   └── test_all.py
├── docs/                    # Documentation
│   ├── README.md
│   ├── QUICKSTART.md
│   ├── USER_GUIDE.md
│   ├── DEVELOPER_GUIDE.md
│   ├── GET_STARTED.txt
│   └── PROJECT_STRUCTURE.txt
├── assets/                  # Icons & resources
│   └── icon.ico
├── config.py               # Configuration
├── requirements.txt        # Dependencies
├── build.py               # Build executables
├── example_usage.py       # Usage examples
└── register_ptdp.bat      # Windows file association
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone/download project
git clone https://github.com/yourusername/PTDP-Protection.git
cd PTDP-Protection

# Install dependencies
pip install -r requirements.txt
```

### 1. Protect File (Seller/Creator)

```python
from core.creator import PTDPCreator

creator = PTDPCreator()
result = creator.create_protected_file(
    input_file="myebook.pdf",
    output_file="myebook.ptdp",
    protection_config={
        'product_id': 'EBOOK001',
        'product_name': 'Trading Guide 2024',
        'master_password': 'SecretKey123',
        'require_online': False,
        'max_devices': 1,
        'expiry_date': None,  # Lifetime
        'view_limit': None    # Unlimited
    }
)
# Result: myebook.ptdp (encrypted file)
```

### 2. Generate License Key

```python
from core.license import LicenseValidator

# Get buyer's device ID (they send this to you)
buyer_device_id = "A1B2C3D4E5F6..."

# Generate license
license_key = LicenseValidator.generate_license(
    product_id='EBOOK001',
    hwid=buyer_device_id,
    expiry_date='LIFETIME'  # or '20251231'
)
# Result: EBOOK001-A1B2C3D4-LIFETIME-F7E8D9C0
```

### 3. Open Protected File (Buyer/User)

```python
from core.reader import PTDPReader

reader = PTDPReader()
result = reader.decrypt_file(
    ptdp_file="myebook.ptdp",
    license_key="EBOOK001-A1B2C3D4-LIFETIME-F7E8D9C0",
    output_file="myebook_decrypted.pdf"
)
# File automatically opens after decryption
```

---

## 🛠️ Build Executables

### Build GUI Applications

```bash
# Build viewer (for end-users)
python build.py viewer

# Build creator (for sellers)
python build.py creator

# Build both
python build.py all
```

**Output:**
- `dist/PTDP-Viewer.exe` - Untuk end-users
- `dist/PTDP-Creator.exe` - Untuk admin/seller

### Create Windows Installer

```bash
# Using Inno Setup (optional)
iscc installer.iss

# Output: installer/PTDP-Viewer-Setup.exe
```

---

## 📖 Usage Workflow

### For Sellers/Content Creators:

1. **Protect your digital product**
   ```bash
   python -m gui.creator
   # Or use PTDP-Creator.exe
   ```

2. **Generate license for buyer**
   - Get buyer's Device ID
   - Generate license key
   - Send license key to buyer

3. **Distribute files**
   - Upload `.ptdp` file (Google Drive, website, etc.)
   - Send PTDP-Viewer.exe to buyer (once)
   - Send unique license key per buyer

### For Buyers/End-Users:

1. **Download PTDP Viewer** (one-time setup)
2. **Download `.ptdp` file** from seller
3. **Open file** in PTDP Viewer
4. **Enter license key** when prompted
5. **View content** - file opens automatically!

---

## 🔑 License Key Format

```
PRODUCT-HWID-EXPIRY-SIGNATURE
EBOOK001-A1B2C3D4-LIFETIME-F7E8D9C0

Components:
- PRODUCT: Product ID (8 chars)
- HWID: Hardware ID (8 chars) - device lock
- EXPIRY: LIFETIME or YYYYMMDD
- SIGNATURE: Cryptographic hash (8 chars)
```

---

## 🌐 License Server (Optional)

### Start Server

```bash
python -m server.api

# Server runs on http://localhost:5000
```

### API Endpoints

- `POST /api/validate` - Validate license
- `POST /api/generate` - Generate license (admin)
- `GET /` - Server status

---

## 📚 Documentation

- **[Quick Start Guide](docs/QUICKSTART.md)** - 5 menit setup
- **[User Guide](docs/USER_GUIDE.md)** - Untuk end-users
- **[Developer Guide](docs/DEVELOPER_GUIDE.md)** - Untuk developers/sellers
- **[Get Started](docs/GET_STARTED.txt)** - Text format guide
- **[Project Structure](docs/PROJECT_STRUCTURE.txt)** - File organization

---

## 🔒 Security Features

✅ **AES-256 Encryption** - Industry standard  
✅ **PBKDF2 Key Derivation** - 200,000 iterations  
✅ **SHA-256 Hashing** - Integrity verification  
✅ **Hardware ID Locking** - Device binding  
✅ **Cryptographic Signatures** - Anti-tampering  
✅ **Offline Validation** - No internet required  
✅ **Online Validation** - Server-based (optional)  

---

## 🎯 Use Cases

- 📖 **Ebooks & Courses** - Protect digital books and training materials
- 🎨 **Templates & Assets** - Protect design files and graphics
- 💼 **Business Documents** - Secure confidential files
- 🎵 **Audio/Video** - Protect media content
- 📊 **Data Files** - Protect spreadsheets and databases
- 🎮 **Game Assets** - Protect game files and mods

---

## ⚙️ Requirements

```
Python 3.8+
cryptography >= 41.0.0
requests >= 2.31.0
psutil >= 5.9.0
flask >= 3.0.0 (for server)
PyInstaller >= 6.0.0 (for building)
```

---

## 🤝 Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

1. Fork the project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🆘 Support

- 📧 Email: support@example.com
- 💬 Discord: [Join Server](#)
- 📖 Documentation: [docs/](docs/)
- 🐛 Issues: [GitHub Issues](#)

---

## 🔮 Roadmap

- [ ] macOS & Linux GUI builds
- [ ] Web-based viewer (browser)
- [ ] Cloud storage integration
- [ ] Payment gateway integration
- [ ] Mobile app support
- [ ] Advanced watermarking
- [ ] Screenshot protection
- [ ] Multi-language support

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Made with ❤️ by PTDP Team**

© 2024 PTDP Protection System - All Rights Reserved
