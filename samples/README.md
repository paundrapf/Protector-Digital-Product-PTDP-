# PTDP Sample Files

This directory contains sample protected files to demonstrate the PTDP system.

## Directory Structure

```
samples/
├── protected/              # Protected .ptdp files
│   ├── trading_ebook.ptdp
│   └── python_course.ptdp
├── licenses/               # License keys and info
│   ├── ebook_license.txt
│   └── course_license.txt
├── sample_ebook.txt       # Original file (for reference)
└── sample_course.txt      # Original file (for reference)
```

## How to Use

### Option 1: GUI Viewer
```bash
python -m gui.viewer
# Then open .ptdp file and enter license key
```

### Option 2: Command Line
```python
from core.reader import PTDPReader

reader = PTDPReader()
result = reader.decrypt_file(
    ptdp_file='samples/protected/trading_ebook.ptdp',
    license_key='[key from licenses/ebook_license.txt]',
    output_file='decrypted_ebook.txt',
    master_password='EbookSecret2024'
)
```

## Sample Files Information

### 1. Trading Ebook (trading_ebook.ptdp)
- **Product ID:** EBOOK001
- **License Type:** Lifetime, Any Device
- **Password:** EbookSecret2024
- **See:** `licenses/ebook_license.txt` for license key

### 2. Python Course (python_course.ptdp)
- **Product ID:** COURSE01
- **License Type:** Device Locked, 1 Year
- **Expiry:** 2025-12-31
- **View Limit:** 100 views
- **Password:** CoursePass2024
- **See:** `licenses/course_license.txt` for license key

## Notes

- The master password is required for decryption
- Device-locked licenses only work on the device they were generated for
- View limits are tracked locally
- Expired licenses cannot open files

## Testing

You can use these sample files to test:
- Opening protected files
- License validation
- Device locking
- Expiry dates
- View limits

Enjoy exploring the PTDP Protection System!
