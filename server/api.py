# server/api.py
"""
PTDP License Server
Flask API untuk online license validation
"""

from flask import Flask, request, jsonify
from datetime import datetime
import hashlib
import json
import os

app = Flask(__name__)

# Simple in-memory database (replace with real database in production)
LICENSES = {}

def load_licenses():
    """Load licenses from file if exists"""
    if os.path.exists('licenses.json'):
        try:
            with open('licenses.json', 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_licenses():
    """Save licenses to file"""
    with open('licenses.json', 'w') as f:
        json.dump(LICENSES, f, indent=2)

# Load existing licenses on startup
LICENSES = load_licenses()

@app.route('/')
def index():
    return jsonify({
        'service': 'PTDP License Server',
        'version': '1.0',
        'status': 'running',
        'total_licenses': len(LICENSES)
    })

@app.route('/api/validate', methods=['POST'])
def validate_license():
    """Validate license key"""
    data = request.json
    license_key = data.get('license_key')
    product_id = data.get('product_id')
    hwid = data.get('hwid')
    
    print(f"🔍 Validating: {license_key} for {product_id}")
    
    # Check if license exists
    if license_key not in LICENSES:
        return jsonify({
            'valid': False,
            'message': 'License key not found in database'
        }), 200
    
    license_data = LICENSES[license_key]
    
    # Check product ID
    if license_data['product_id'] != product_id:
        return jsonify({
            'valid': False,
            'message': 'License key is for a different product'
        }), 200
    
    # Check status
    if license_data.get('status') != 'active':
        return jsonify({
            'valid': False,
            'message': f"License is {license_data.get('status', 'inactive')}"
        }), 200
    
    # Check expiry
    if license_data.get('expiry'):
        try:
            exp_date = datetime.fromisoformat(license_data['expiry'])
            if datetime.now() > exp_date:
                return jsonify({
                    'valid': False,
                    'message': 'License expired'
                }), 200
        except:
            pass
    
    # Check device limit
    if hwid not in license_data.get('active_devices', []):
        if len(license_data.get('active_devices', [])) >= license_data.get('max_devices', 1):
            return jsonify({
                'valid': False,
                'message': 'Device limit reached. Contact seller for additional device slots.'
            }), 200
        else:
            # Add this device
            if 'active_devices' not in license_data:
                license_data['active_devices'] = []
            license_data['active_devices'].append(hwid)
            save_licenses()
    
    # Update last used
    license_data['last_used'] = datetime.now().isoformat()
    save_licenses()
    
    return jsonify({
        'valid': True,
        'message': 'License valid',
        'expiry': license_data.get('expiry'),
        'devices_used': len(license_data.get('active_devices', [])),
        'max_devices': license_data.get('max_devices', 1)
    }), 200

@app.route('/api/generate', methods=['POST'])
def generate_license():
    """Generate new license (admin endpoint - should be protected!)"""
    data = request.json
    
    # Simple auth (replace with proper auth in production)
    api_key = request.headers.get('X-API-Key')
    if api_key != 'YOUR_SECRET_API_KEY_HERE':  # Change this!
        return jsonify({'error': 'Unauthorized'}), 401
    
    product_id = data.get('product_id')
    hwid = data.get('hwid', 'ANY')
    expiry = data.get('expiry', None)
    max_devices = data.get('max_devices', 1)
    
    # Generate license key using same method as core.license
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from core.license import LicenseValidator
    
    license_key = LicenseValidator.generate_license(
        product_id=product_id,
        hwid=hwid,
        expiry_date=expiry if expiry else "LIFETIME"
    )
    
    # Store in database
    LICENSES[license_key] = {
        'product_id': product_id,
        'hwid': hwid[:8] if hwid != 'ANY' else 'ANY',
        'expiry': expiry,
        'max_devices': max_devices,
        'active_devices': [],
        'created_at': datetime.now().isoformat(),
        'status': 'active'
    }
    
    save_licenses()
    
    return jsonify({
        'success': True,
        'license_key': license_key,
        'product_id': product_id
    }), 200

@app.route('/api/deactivate', methods=['POST'])
def deactivate_license():
    """Deactivate a license (admin endpoint)"""
    data = request.json
    
    # Simple auth
    api_key = request.headers.get('X-API-Key')
    if api_key != 'YOUR_SECRET_API_KEY_HERE':
        return jsonify({'error': 'Unauthorized'}), 401
    
    license_key = data.get('license_key')
    
    if license_key in LICENSES:
        LICENSES[license_key]['status'] = 'deactivated'
        save_licenses()
        return jsonify({'success': True, 'message': 'License deactivated'}), 200
    else:
        return jsonify({'error': 'License not found'}), 404

if __name__ == '__main__':
    print("🚀 PTDP License Server")
    print("=" * 50)
    print("Server running on http://localhost:5000")
    print(f"Total licenses: {len(LICENSES)}")
    print("\nEndpoints:")
    print("  GET  /                - Server info")
    print("  POST /api/validate    - Validate license")
    print("  POST /api/generate    - Generate license (admin)")
    print("  POST /api/deactivate  - Deactivate license (admin)")
    print("\n⚠️  Remember to change the API key in production!")
    print("=" * 50)
    
    app.run(debug=True, port=5000)
