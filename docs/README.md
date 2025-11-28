# PTDP Protection System
## Protected Digital Product Format

🔒 **Sistem proteksi file digital dengan enkripsi, license validation, dan hardware lock**

---

## 📁 Struktur Project

```
ptdp-protection/
├── core/                    # Core functionality
│   ├── __init__.py
│   ├── creator.py          # File protection/encryption
│   ├── reader.py           # File decryption/viewing
│   ├── license.py          # License generation & validation
│   └── hwid.py             # Hardware ID detection
├── server/                  # License server API
│   ├── __init__.py
│   ├── api.py              # Flask API endpoints
│   └── database.py         # Database management
├── gui/                     # GUI Applications
│   ├── viewer.py           # End-user viewer (public)
│   ├── creator.py          # Admin creator tool
│   └── admin.py            # License management dashboard
├── tests/                   # Unit tests
│   └── test_all.py
├── assets/                  # Icons & resources
│   └── icon.ico
├── docs/                    # Documentation
│   ├── USER_GUIDE.md
│   └── DEVELOPER_GUIDE.md
├── requirements.txt         # Python dependencies
├── build.py                # Build executables
├── installer.iss           # Windows installer script
├── register_ptdp.bat       # Registry file association
└── config.py               # Configuration settings
```

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone/download project
cd ptdp-protection

# Install dependencies
pip install -r requirements.txt
```

### 2. Protect Your First File

```python
from core.creator import PTDPCreator

creator = PTDPCreator()

# Protect file
creator.create_protected_file(
    input_file="ebook.pdf",
    output_file="ebook.ptdp",
    config={
        'product_id': 'EBOOK001',
        'product_name': 'Advanced Trading Guide',
        'master_password': 'your_secret_password',
        'require_online': False,
        'max_devices': 1
    }
)
```

### 3. Generate License Key

```python
from core.license import LicenseValidator

license_key = LicenseValidator.generate_license(
    product_id="EBOOK001",
    hwid="12345678",  # Buyer's device ID
    expiry_date="LIFETIME"
)

print(f"License: {license_key}")
```

### 4. Open Protected File

```python
from core.reader import PTDPReader

reader = PTDPReader()

result = reader.decrypt_file(
    ptdp_file="ebook.ptdp",
    license_key="EBOOK001-12345678-LIFETIME-A1B2C3D4",
    output_file="ebook_unlocked.pdf"
)

if result['success']:
    print("✅ File unlocked!")
```

---

## 🛠️ Build untuk Distribution

### Build Executables

```bash
# Build viewer dan creator
python build.py
```

Output:
- `dist/PTDP-Viewer.exe` - Untuk end-users
- `dist/PTDP-Creator.exe` - Untuk admin/seller

### Create Installer (Windows)

1. Install [Inno Setup](https://jrsoftware.org/isdl.php)
2. Run: `iscc installer.iss`
3. Output: `installer/PTDP-Viewer-Setup.exe`

---

## 📦 Features

### Protection Features
- ✅ AES-256 encryption
- ✅ Hardware ID lock (device-specific)
- ✅ Online license validation
- ✅ Offline mode support
- ✅ Expiry date support
- ✅ View limit tracking
- ✅ Multi-device support
- ✅ File integrity check
- ✅ Watermarking support

### License Types
- **Single Device** - 1 device only
- **Multi Device** - Up to N devices
- **Lifetime** - Never expires
- **Time-Limited** - Expires after date

---

## 🌐 License Server

### Start Server

```bash
cd server
python api.py
```

Server runs on `http://localhost:5000`

### API Endpoints

```
POST /api/validate
- Validate license key
- Body: {license_key, product_id, hwid}

POST /api/generate
- Generate new license (admin)
- Body: {product_id, hwid, expiry, max_devices}
```

---

## 💻 For End-Users

### How to Open .ptdp Files

1. Download & install PTDP Viewer
2. Double-click any `.ptdp` file
3. Enter your license key
4. File will open in default app

### Get Your Device ID

Open PTDP Viewer, device ID shown at bottom.

---

## 👨‍💻 For Developers/Sellers

### Workflow

1. **Create Protected File**
   ```bash
   python gui/creator.py
   ```

2. **Upload to Distribution**
   - Upload `.ptdp` file to Google Drive/website
   - Keep master password secret!

3. **Generate License for Buyer**
   ```python
   # Get buyer's device ID first
   license = LicenseValidator.generate_license(
       product_id="PROD001",
       hwid=buyer_device_id,
       expiry_date="20251231"
   )
   ```

4. **Send License to Buyer**
   - Email the license key
   - Buyer enters it in PTDP Viewer

---

## 🔧 Configuration

Edit `config.py`:

```python
# Encryption
MASTER_SALT = "your_custom_salt"
KDF_ITERATIONS = 200000

# Server
API_URL = "http://your-server.com/api"
API_KEY = "your_api_key"

# Features
ENABLE_ONLINE_CHECK = True
ENABLE_HWID_LOCK = True
ENABLE_VIEW_LIMIT = True
```

---

## 📖 Documentation

- [User Guide](docs/USER_GUIDE.md) - For end-users
- [Developer Guide](docs/DEVELOPER_GUIDE.md) - For developers

---

## 🔐 Security Notes

1. **Master Password** - Keep secret, used for all files
2. **API Keys** - Rotate regularly
3. **HWID Lock** - Can't transfer to other devices
4. **Offline Mode** - Less secure but more convenient

---

## 🐛 Troubleshooting

### "Invalid PTDP file"
- File corrupted or wrong format
- Try re-downloading

### "License validation failed"
- Check internet connection (online mode)
- Verify license key format
- Check device ID matches

### "Device limit reached"
- License used on max devices
- Contact seller for new license

---

## 📝 License

MIT License - Free to use and modify

---

## 👤 Author

Created by Firlan - [GitHub](#)

---

## 🤝 Support

Need help? Contact: support@example.com
