# core/updater.py
"""
Auto-Update Module for PTDP Applications
Checks GitHub Releases for new versions and auto-updates
"""

import os
import sys
import json
import requests
import tempfile
import subprocess
import threading
from pathlib import Path

# Version info
CURRENT_VERSION = "1.0.2"
GITHUB_REPO = "paundrapf/Protector-Digital-Product-PTDP-"
GITHUB_API = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"


class AutoUpdater:
    """Auto-update functionality for PTDP apps"""
    
    def __init__(self, app_name="PTDP", current_version=CURRENT_VERSION):
        self.app_name = app_name
        self.current_version = current_version
        self.github_api = GITHUB_API
        self.github_repo = GITHUB_REPO
        self.update_available = False
        self.latest_version = None
        self.download_url = None
        self.release_notes = ""
        
    def check_for_updates(self, callback=None):
        """
        Check GitHub for new releases
        
        Args:
            callback: Function to call with result (update_available, version, notes)
        
        Returns:
            tuple: (update_available: bool, latest_version: str, release_notes: str)
        """
        try:
            response = requests.get(
                self.github_api,
                headers={'Accept': 'application/vnd.github.v3+json'},
                timeout=10
            )
            
            if response.status_code != 200:
                return False, self.current_version, "Could not check for updates"
            
            data = response.json()
            self.latest_version = data.get('tag_name', '').lstrip('v')
            self.release_notes = data.get('body', 'No release notes')
            
            # Find the right asset for this app
            assets = data.get('assets', [])
            for asset in assets:
                asset_name = asset.get('name', '')
                # Match Creator or Viewer based on app_name
                if self.app_name == "Creator" and "Creator" in asset_name:
                    self.download_url = asset.get('browser_download_url')
                    break
                elif self.app_name == "Viewer" and "Viewer" in asset_name:
                    self.download_url = asset.get('browser_download_url')
                    break
            
            # Compare versions
            self.update_available = self._is_newer_version(self.latest_version)
            
            if callback:
                callback(self.update_available, self.latest_version, self.release_notes)
            
            return self.update_available, self.latest_version, self.release_notes
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error: {str(e)}"
            if callback:
                callback(False, self.current_version, error_msg)
            return False, self.current_version, error_msg
        except Exception as e:
            error_msg = f"Error checking updates: {str(e)}"
            if callback:
                callback(False, self.current_version, error_msg)
            return False, self.current_version, error_msg
    
    def check_for_updates_async(self, callback):
        """Check for updates in background thread"""
        thread = threading.Thread(target=self.check_for_updates, args=(callback,))
        thread.daemon = True
        thread.start()
    
    def _is_newer_version(self, latest):
        """Compare version strings"""
        try:
            current_parts = [int(x) for x in self.current_version.split('.')]
            latest_parts = [int(x) for x in latest.split('.')]
            
            # Pad shorter version with zeros
            while len(current_parts) < len(latest_parts):
                current_parts.append(0)
            while len(latest_parts) < len(current_parts):
                latest_parts.append(0)
            
            return latest_parts > current_parts
        except:
            return False
    
    def download_update(self, progress_callback=None):
        """
        Download the update file
        
        Args:
            progress_callback: Function(downloaded, total) for progress updates
        
        Returns:
            str: Path to downloaded file, or None if failed
        """
        if not self.download_url:
            return None
        
        try:
            # Create temp file
            temp_dir = tempfile.gettempdir()
            filename = f"PTDP-{self.app_name}-Update-{self.latest_version}.exe"
            temp_path = os.path.join(temp_dir, filename)
            
            # Download with progress
            response = requests.get(self.download_url, stream=True, timeout=60)
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if progress_callback:
                            progress_callback(downloaded, total_size)
            
            return temp_path
            
        except Exception as e:
            print(f"Download error: {e}")
            return None
    
    def apply_update(self, update_path):
        """
        Apply the update by replacing current executable
        
        Args:
            update_path: Path to downloaded update file
        
        Returns:
            bool: Success status
        """
        if not update_path or not os.path.exists(update_path):
            return False
        
        try:
            # Get current executable path
            if getattr(sys, 'frozen', False):
                # Running as compiled exe
                current_exe = sys.executable
            else:
                # Running as script - can't auto-update
                print("Auto-update only works with compiled .exe")
                return False
            
            # Create update script that will:
            # 1. Wait for current app to close
            # 2. Replace the exe
            # 3. Restart the app
            
            batch_script = f'''@echo off
timeout /t 2 /nobreak > nul
copy /y "{update_path}" "{current_exe}"
del "{update_path}"
start "" "{current_exe}"
del "%~f0"
'''
            
            batch_path = os.path.join(tempfile.gettempdir(), "ptdp_update.bat")
            with open(batch_path, 'w') as f:
                f.write(batch_script)
            
            # Run the batch script and exit
            subprocess.Popen(
                ['cmd', '/c', batch_path],
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
            )
            
            return True
            
        except Exception as e:
            print(f"Update apply error: {e}")
            return False


def get_version():
    """Get current app version"""
    return CURRENT_VERSION


def set_version(version):
    """Set current version (for testing)"""
    global CURRENT_VERSION
    CURRENT_VERSION = version


# CLI for testing
if __name__ == "__main__":
    print("PTDP Auto-Updater Test")
    print("=" * 40)
    print(f"Current Version: {CURRENT_VERSION}")
    
    updater = AutoUpdater("Viewer", CURRENT_VERSION)
    available, version, notes = updater.check_for_updates()
    
    print(f"\nUpdate Available: {available}")
    print(f"Latest Version: {version}")
    print(f"Release Notes: {notes[:200]}...")
