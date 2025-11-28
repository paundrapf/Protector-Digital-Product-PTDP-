# config.py
# PTDP Protection System Configuration

import os

# ========================
# ENCRYPTION SETTINGS
# ========================
MASTER_SALT = b"ptdp_salt_2024_firlan"  # Ganti dengan random salt
SECRET_KEY = "YOUR_SECRET_KEY_2024"  # Untuk license signature
KDF_ITERATIONS = 200000  # PBKDF2 iterations

# ========================
# LICENSE SERVER
# ========================
API_URL = "http://localhost:5000/api"  # Ganti dengan server production
API_TIMEOUT = 5  # seconds

# ========================
# FILE SETTINGS
# ========================
MAGIC_BYTES = b'PTDP'
VERSION = b'2.0'
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500 MB

# ========================
# FEATURES
# ========================
ENABLE_ONLINE_VALIDATION = True
ENABLE_HWID_LOCK = True
ENABLE_VIEW_LIMIT = True
ENABLE_WATERMARK = True

# ========================
# DEFAULT VALUES
# ========================
DEFAULT_MAX_DEVICES = 1
DEFAULT_LICENSE_TYPE = "premium"
DEFAULT_EXPIRY = "LIFETIME"

# ========================
# PATHS
# ========================
TEMP_DIR = os.path.join(os.path.expanduser("~"), ".ptdp_temp")
USAGE_FILE = os.path.join(TEMP_DIR, ".ptdp_usage.json")

# Create temp directory if not exists
os.makedirs(TEMP_DIR, exist_ok=True)

# ========================
# DATABASE (for server)
# ========================
DB_PATH = "licenses.db"
DB_URL = f"sqlite:///{DB_PATH}"

# ========================
# SECURITY
# ========================
# PDF-only protection (Gen-Z focus)
ALLOWED_EXTENSIONS = [
    '.pdf'  # Currently only PDF files are supported
]

# Future support (coming soon)
# '.docx', '.xlsx', '.pptx', '.epub'

# ========================
# BRANDING
# ========================
APP_NAME = "PTDP Viewer"
APP_VERSION = "1.0.0"
COMPANY_NAME = "Your Company"
SUPPORT_EMAIL = "support@example.com"
