# PTPD Protection - Quick Start Guide

Get started with PTPD in 5 minutes!

---

## 🚀 For Sellers/Creators (Protect Your Products)

### Step 1: Install
```bash
cd ptpd-protection
pip install -r requirements.txt
```

### Step 2: Protect a File
```bash
python gui/creator.py
```

1. Click "Browse" and select your file (PDF, video, etc.)
2. Enter Product ID: `EBOOK001`
3. Enter Product Name: `My Amazing Ebook`
4. Enter Master Password: `MySecret123` (SAVE THIS!)
5. Click "Create Protected File"

✅ You now have a `.ptpd` file!

### Step 3: Generate License for Buyer

```bash
python core/license.py
```

Or use Python:
```python
from core.license import LicenseValidator

license = LicenseValidator.generate_license(
    product_id='EBOOK001',
    hwid=None,  # Any device
    expiry_date='LIFETIME'
)

print(f"Send this to buyer: {license}")
```

### Step 4: Distribute

1. Upload `.ptpd` file to Google Drive / your website
2. Send download link + license key to buyer
3. Buyer downloads PTPD Viewer and opens the file

✅ Done!

---

## 👤 For Buyers (Open Protected Files)

### Step 1: Get PTPD Viewer

Download `PTPD-Viewer.exe` from the seller

### Step 2: Open Protected File

1. Run `PTPD-Viewer.exe`
2. Click "Open PTPD File"
3. Select your `.ptpd` file
4. Enter license key (from seller)
5. Click "Unlock & View File"

✅ File opens!

---

## 🖥️ Need Your Device ID?

Open PTPD Viewer - it's shown at the bottom. Send this to seller if you need a device-locked license.

---

## 🔧 Advanced: Run License Server

### Start Server
```bash
cd server
python api.py
```

Server runs on `http://localhost:5000`

### Update config.py
```python
API_URL = "http://your-server.com/api"
```

### Enable Online Validation
When protecting files, set:
```python
'require_online': True
```

---

## 📦 Build Executables

```bash
python build.py
```

Creates:
- `dist/PTPD-Viewer.exe` → Give to users
- `dist/PTPD-Creator.exe` → Keep for yourself

---

## ❓ Common Issues

**"Module not found"**
```bash
pip install -r requirements.txt
```

**"Invalid license"**
- Check SECRET_KEY in config.py matches on both sides
- Verify product ID is correct

**"Can't open file"**
- Install app for file type (PDF reader, video player, etc.)

---

## 📚 Learn More

- [README.md](README.md) - Full documentation
- [USER_GUIDE.md](docs/USER_GUIDE.md) - For end-users
- [DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md) - For developers
- [example_usage.py](example_usage.py) - Code examples

---

## 🆘 Need Help?

- Run tests: `python tests/test_all.py`
- See examples: `python example_usage.py`
- Check docs folder for detailed guides

---

That's it! You're ready to protect and distribute your digital products! 🎉
