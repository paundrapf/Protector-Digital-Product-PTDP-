<p align="center">
  <img src="assets/icons/installer_icon.svg" width="120" alt="PTDP Logo">
</p>

<h1 align="center">PTDP Protection System</h1>

<p align="center">
  <strong>Protect Your Digital Products with AES-256 Encryption</strong>
</p>

<p align="center">
  <a href="https://github.com/paundrapf/Protector-Digital-Product-PTDP-/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/paundrapf/Protector-Digital-Product-PTDP-/build.yml?style=for-the-badge&logo=github&label=BUILD" alt="Build Status">
  </a>
  <a href="https://github.com/paundrapf/Protector-Digital-Product-PTDP-/releases/latest">
    <img src="https://img.shields.io/github/v/release/paundrapf/Protector-Digital-Product-PTDP-?style=for-the-badge&logo=github&color=FF4D6D&label=VERSION" alt="Latest Release">
  </a>
  <a href="https://github.com/paundrapf/Protector-Digital-Product-PTDP-/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/LICENSE-MIT-blue?style=for-the-badge" alt="License">
  </a>
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-features">Features</a> •
  <a href="#-download">Download</a> •
  <a href="#-faq">FAQ</a>
</p>

---

## What is PTDP?

**PTDP (Protected Digital Product)** is a custom file format (`.ptdp`) designed to protect digital products like ebooks, courses, templates, and premium content.

| For Sellers | For Buyers |
|-------------|------------|
| Protect your digital products from piracy. Create encrypted files that can only be opened with valid license keys. | Securely read protected content. Download, enter your license key, and enjoy! |

---

## Features

| Feature | Description |
|---------|-------------|
| **AES-256 Encryption** | Industry-standard encryption |
| **License System** | Unique keys for each customer |
| **Hardware Lock** | Bind license to specific devices |
| **Expiry Date** | Set content expiration |
| **View Limit** | Control how many times content can be viewed |
| **Auto-Update** | Apps automatically check for updates |
| **In-App PDF Reader** | Secure PDF viewing with anti-screenshot |
| **Modern UI** | Dark theme interface |

---

## Download

<table>
<tr>
<td align="center" width="50%">
<h3>PTDP Viewer</h3>
<p><em>For Buyers - Read protected content</em></p>
<a href="https://github.com/paundrapf/Protector-Digital-Product-PTDP-/releases/latest/download/PTDP-Viewer-Windows.exe">
<img src="https://img.shields.io/badge/DOWNLOAD-VIEWER-3B82F6?style=for-the-badge&logo=windows" alt="Download Viewer">
</a>
</td>
<td align="center" width="50%">
<h3>PTDP Creator</h3>
<p><em>For Sellers - Protect your products</em></p>
<a href="https://github.com/paundrapf/Protector-Digital-Product-PTDP-/releases/latest/download/PTDP-Creator-Windows.exe">
<img src="https://img.shields.io/badge/DOWNLOAD-CREATOR-FF4D6D?style=for-the-badge&logo=windows" alt="Download Creator">
</a>
</td>
</tr>
</table>

> **Note:** Windows may show SmartScreen warning on first run. Click **"More info"** → **"Run anyway"**

---

## Quick Start

### For Buyers (Reading Protected Files)

1. Download PTDP-Viewer-Windows.exe
2. Double-click to run (no installation needed)
3. Open .ptdp file
4. Enter your license key
5. Read your content

### For Sellers (Creating Protected Files)

1. Download PTDP-Creator-Windows.exe
2. Double-click to run
3. Select PDF file to protect
4. Configure protection settings
5. Generate license keys for customers
6. Distribute .ptdp file + license keys

---

## How It Works

```
Original PDF → PTDP Creator → Encrypted .ptdp + License Keys
                                    ↓
                            PTDP Viewer + License Key → View Content
```

### Technical Details

- PDF content encrypted using AES-256
- Encryption key derived via PBKDF2
- Metadata stored in file header
- License validation checks hardware ID, expiry, view count

### Security Features

- Anti-Screenshot: Windows Display Affinity protection
- Anti-Copy: Keyboard shortcuts disabled in viewer
- Hardware Binding: License tied to specific machine
- Expiry Control: Time-based license expiration

---

## Project Structure

```
PTDP-Protection/
├── core/                    # Core modules
│   ├── creator.py          # File encryption
│   ├── reader.py           # File decryption
│   ├── license.py          # License validation
│   ├── hwid.py             # Hardware ID detection
│   └── updater.py          # Auto-update system
├── gui/                     # GUI applications
│   ├── viewer_modern.py    # Secure PDF viewer
│   └── creator_modern.py   # Creator interface
├── assets/icons/            # App icons
├── website/                 # Landing page
├── config.py               # Configuration
├── requirements.txt        # Dependencies
├── viewer.py               # Viewer entry point
└── creator.py              # Creator entry point
```

---

## FAQ

<details>
<summary><strong>Why does Windows show a warning?</strong></summary>

Windows SmartScreen shows warnings for unsigned applications. To remove this, the app needs a code signing certificate. The app is safe - verify by checking the source code.

Workaround: Click "More info" → "Run anyway"
</details>

<details>
<summary><strong>Can I use one license on multiple devices?</strong></summary>

By default, licenses are bound to one device. Sellers can configure multi-device licenses using the ANYDEVIC option in Creator.
</details>

<details>
<summary><strong>What happens when license expires?</strong></summary>

The viewer will show an "Expired License" message. Users need to contact the seller for renewal.
</details>

---

## Development

```bash
# Clone repository
git clone https://github.com/paundrapf/Protector-Digital-Product-PTDP-.git
cd Protector-Digital-Product-PTDP-

# Install dependencies
pip install -r requirements.txt

# Run viewer
python viewer.py

# Run creator
python creator.py
```

---

## License

MIT License - see [LICENSE](LICENSE) for details.
