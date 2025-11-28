# gui/viewer.py
"""
PTPD Viewer - End-User Application
GUI untuk membuka dan view protected .ptpd files
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.reader import PTPDReader
from core.hwid import HardwareID

class PTPDViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("PTPD Viewer - Protected Digital Product")
        self.root.geometry("900x700")
        self.root.configure(bg='#2b2b2b')
        
        # Set icon (if exists)
        try:
            icon_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'icon.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
        
        self.reader = PTPDReader()
        self.current_file = None
        self.current_metadata = None
        
        self.setup_ui()
        
        # Check if file was passed as argument (double-click support)
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
            if file_path.endswith('.ptpd'):
                self.root.after(100, lambda: self.open_file(file_path))
    
    def setup_ui(self):
        """Setup user interface"""
        
        # ============= HEADER =============
        header_frame = tk.Frame(self.root, bg='#1e1e1e', height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🔒 PTPD Viewer",
            font=("Arial", 24, "bold"),
            bg='#1e1e1e',
            fg='#00ff88'
        )
        title_label.pack(pady=20)
        
        # ============= MAIN CONTENT =============
        content_frame = tk.Frame(self.root, bg='#2b2b2b')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Button Frame
        button_frame = tk.Frame(content_frame, bg='#2b2b2b')
        button_frame.pack(pady=15)
        
        open_btn = tk.Button(
            button_frame,
            text="📂 Open PTPD File",
            command=self.open_file_dialog,
            bg='#00ff88',
            fg='#000000',
            font=("Arial", 13, "bold"),
            padx=30,
            pady=12,
            cursor='hand2',
            relief=tk.FLAT,
            borderwidth=0
        )
        open_btn.pack(side=tk.LEFT, padx=5)
        
        info_btn = tk.Button(
            button_frame,
            text="ℹ️  Help",
            command=self.show_help,
            bg='#4a4a4a',
            fg='#ffffff',
            font=("Arial", 13, "bold"),
            padx=30,
            pady=12,
            cursor='hand2',
            relief=tk.FLAT
        )
        info_btn.pack(side=tk.LEFT, padx=5)
        
        # ============= INFO AREA =============
        info_frame = tk.LabelFrame(
            content_frame,
            text="  Product Information  ",
            bg='#363636',
            fg='#00ff88',
            font=("Arial", 11, "bold"),
            padx=15,
            pady=15
        )
        info_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.info_text = scrolledtext.ScrolledText(
            info_frame,
            bg='#2b2b2b',
            fg='#ffffff',
            font=("Consolas", 10),
            wrap=tk.WORD,
            state=tk.DISABLED,
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # Initial welcome message
        welcome_msg = """
╔═══════════════════════════════════════════════════════════════╗
║                    Welcome to PTPD Viewer!                    ║
╚═══════════════════════════════════════════════════════════════╝

👋 This application helps you open protected digital products (.ptpd files)

📖 How to use:
   1. Click "Open PTPD File" button above
   2. Select your .ptpd file
   3. Enter your license key when prompted
   4. The file will open automatically

💡 Tips:
   • You need a valid license key to open protected files
   • License keys are provided by the seller
   • Each file may require a different license key
   • Your Device ID is shown at the bottom (needed for some licenses)

🔒 Security:
   • All files are encrypted with AES-256
   • License validation ensures only authorized access
   • Your privacy and data are protected

Need help? Click the "Help" button above or contact the seller.
        """
        self.update_info(welcome_msg.strip(), '#cccccc')
        
        # ============= LICENSE FRAME =============
        license_frame = tk.LabelFrame(
            content_frame,
            text="  License Key  ",
            bg='#363636',
            fg='#ff6b35',
            font=("Arial", 11, "bold"),
            padx=15,
            pady=15
        )
        license_frame.pack(fill=tk.X, pady=10)
        
        # License entry with label
        entry_container = tk.Frame(license_frame, bg='#363636')
        entry_container.pack(fill=tk.X)
        
        tk.Label(
            entry_container,
            text="Enter your license key:",
            bg='#363636',
            fg='#cccccc',
            font=("Arial", 9)
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.license_entry = tk.Entry(
            entry_container,
            bg='#1e1e1e',
            fg='#ffffff',
            font=("Consolas", 12),
            insertbackground='#ffffff',
            relief=tk.FLAT,
            borderwidth=0
        )
        self.license_entry.pack(fill=tk.X, ipady=8)
        
        # Unlock button
        unlock_btn = tk.Button(
            license_frame,
            text="🔓 Unlock & View File",
            command=self.unlock_file,
            bg='#ff6b35',
            fg='#ffffff',
            font=("Arial", 12, "bold"),
            padx=25,
            pady=10,
            cursor='hand2',
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        unlock_btn.pack(pady=(15, 5))
        self.unlock_btn = unlock_btn
        
        # ============= FOOTER =============
        footer_frame = tk.Frame(self.root, bg='#1e1e1e', height=50)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)
        
        device_id = HardwareID.get_simple_hwid()
        hwid_label = tk.Label(
            footer_frame,
            text=f"🖥️  Your Device ID: {device_id[:24]}... (click to copy)",
            font=("Arial", 9),
            bg='#1e1e1e',
            fg='#888888',
            cursor='hand2'
        )
        hwid_label.pack(pady=15)
        hwid_label.bind('<Button-1>', lambda e: self.copy_device_id(device_id))
        
        version_label = tk.Label(
            footer_frame,
            text="PTPD Viewer v1.0  |  © 2024",
            font=("Arial", 8),
            bg='#1e1e1e',
            fg='#555555'
        )
        version_label.place(relx=1.0, rely=1.0, anchor=tk.SE, x=-10, y=-5)
    
    def update_info(self, text, color='#ffffff'):
        """Update info text area"""
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, text)
        self.info_text.config(state=tk.DISABLED, fg=color)
    
    def open_file_dialog(self):
        """Open file dialog untuk select .ptpd file"""
        file_path = filedialog.askopenfilename(
            title="Select PTPD File",
            filetypes=[("PTPD Files", "*.ptpd"), ("All Files", "*.*")]
        )
        if file_path:
            self.open_file(file_path)
    
    def open_file(self, file_path):
        """Open dan display info .ptpd file"""
        self.current_file = file_path
        
        try:
            # Read metadata without decrypting
            metadata = self.reader.read_metadata(file_path)
            self.current_metadata = metadata
            
            # Build info display
            expiry_info = "♾️  LIFETIME" if not metadata.get('expiry_date') else f"⏰ {metadata['expiry_date']}"
            online_info = "🌐 ONLINE CHECK REQUIRED" if metadata.get('require_online') else "💻 OFFLINE MODE"
            device_info = f"📱 Max {metadata.get('max_devices', 1)} device(s)" if metadata.get('max_devices') else ""
            view_limit_info = f"👁️  {metadata.get('view_limit')} views max" if metadata.get('view_limit') else ""
            
            info = f"""
╔═══════════════════════════════════════════════════════════════╗
║              PROTECTED DIGITAL PRODUCT LOADED                 ║
╚═══════════════════════════════════════════════════════════════╝

📦 Product Name     : {metadata['product_name']}
🆔 Product ID       : {metadata['product_id']}
📌 Version          : {metadata['version']}
💎 License Type     : {metadata['license_type'].upper()}

📄 Original Format  : {metadata['original_extension']}
📊 File Size        : {metadata['file_size'] / 1024:.2f} KB
📅 Created          : {metadata['created_at'][:10]}

{expiry_info}
{online_info}
{device_info}
{view_limit_info}

╔═══════════════════════════════════════════════════════════════╗
║          Enter your license key below to unlock               ║
╚═══════════════════════════════════════════════════════════════╝

💡 Your license key format: XXXX-XXXX-XXXX-XXXX
🔒 Your Device ID: {HardwareID.get_simple_hwid()[:24]}...

⚠️  Note: Invalid license keys will be rejected
            """
            
            self.update_info(info.strip(), '#00ff88')
            
            # Enable unlock button
            self.unlock_btn.config(state=tk.NORMAL)
            
            # Auto-focus license entry
            self.license_entry.focus()
            self.license_entry.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file:\n\n{str(e)}")
            self.current_file = None
            self.current_metadata = None
    
    def unlock_file(self):
        """Unlock dan open file dengan license key"""
        if not self.current_file:
            messagebox.showwarning("No File", "Please open a PTPD file first")
            return
        
        license_key = self.license_entry.get().strip()
        if not license_key:
            messagebox.showwarning("No License", "Please enter your license key")
            self.license_entry.focus()
            return
        
        # Show loading state
        self.unlock_btn.config(state=tk.DISABLED, text="🔄 Processing...")
        self.update_info(
            "🔄 Validating license and decrypting file...\n\nPlease wait, this may take a few seconds...",
            '#ffaa00'
        )
        self.root.update()
        
        # Try to decrypt
        result = self.reader.decrypt_file(
            self.current_file,
            license_key,
            output_file=None  # Keep in memory
        )
        
        # Re-enable button
        self.unlock_btn.config(state=tk.NORMAL, text="🔓 Unlock & View File")
        
        if result['success']:
            # Success - open the decrypted file
            self.open_decrypted_content(result)
        else:
            # Failed
            error_msg = f"""
╔═══════════════════════════════════════════════════════════════╗
║                    ❌ UNLOCK FAILED                            ║
╚═══════════════════════════════════════════════════════════════╝

{result['error']}

📝 Common issues:
   • Wrong license key format or value
   • License key for different product
   • Device ID mismatch (device-locked license)
   • License expired or view limit reached
   • Internet connection required but not available

💡 Solutions:
   • Double-check your license key
   • Contact the seller for support
   • Verify your Device ID matches the license

🔒 Your Device ID: {HardwareID.get_simple_hwid()[:32]}...
            """
            self.update_info(error_msg.strip(), '#ff6b35')
            messagebox.showerror("Unlock Failed", result['error'])
    
    def open_decrypted_content(self, result):
        """Open decrypted content dengan default app"""
        content = result['content']
        metadata = result['metadata']
        extension = metadata['original_extension']
        
        # Save to temp file
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension,
            prefix='ptpd_'
        )
        temp_file.write(content)
        temp_file.close()
        
        success_msg = f"""
╔═══════════════════════════════════════════════════════════════╗
║                ✅ FILE UNLOCKED SUCCESSFULLY!                  ║
╚═══════════════════════════════════════════════════════════════╝

📖 Product: {metadata['product_name']}
📄 Type: {extension}
📊 Size: {len(content) / 1024:.2f} KB

🎉 The file is now opening in your default application...

💾 Temporary location: {temp_file.name}

{f"⚠️  {metadata['watermark']}" if metadata.get('watermark') else ""}

ℹ️  Note: The file will be automatically deleted when you close it.
        """
        
        self.update_info(success_msg.strip(), '#00ff88')
        
        # Open with default application
        import platform
        import subprocess
        
        try:
            if platform.system() == 'Windows':
                os.startfile(temp_file.name)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.call(['open', temp_file.name])
            else:  # Linux
                subprocess.call(['xdg-open', temp_file.name])
            
            messagebox.showinfo(
                "Success!",
                f"File unlocked and opened!\n\n{metadata['product_name']}"
            )
        except Exception as e:
            messagebox.showinfo(
                "Manual Open Required",
                f"File decrypted successfully!\n\nPlease open manually:\n{temp_file.name}"
            )
    
    def copy_device_id(self, device_id):
        """Copy device ID ke clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(device_id)
        messagebox.showinfo("Copied!", f"Device ID copied to clipboard:\n\n{device_id[:32]}...")
    
    def show_help(self):
        """Show help dialog"""
        help_text = """
🔒 PTPD Viewer - Help Guide

WHAT IS PTPD?
PTPD (Protected Digital Product) is a secure file format for
protecting digital products like ebooks, courses, software, etc.

HOW TO OPEN A .PTPD FILE:
1. Click "Open PTPD File" button
2. Select your .ptpd file
3. Enter the license key provided by the seller
4. Click "Unlock & View File"
5. The file will open in its default application

LICENSE KEY FORMAT:
License keys look like: XXXX-XXXX-XXXX-XXXX
Example: EBOOK001-A1B2C3D4-20251231-E5F6G7H8

DEVICE ID:
Some licenses are locked to specific devices. Your Device ID
is shown at the bottom of this window. Share this with the
seller if you need a device-locked license.

TROUBLESHOOTING:
• "Invalid license key" → Check the key format and value
• "Device mismatch" → License is for a different device
• "License expired" → Contact seller for renewal
• "View limit reached" → Maximum views exceeded

CONTACT:
For support, contact the product seller with:
• Your license key
• Your Device ID  
• Product name
• Error message (if any)

© 2024 PTPD Protection System
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Help - PTPD Viewer")
        help_window.geometry("600x500")
        help_window.configure(bg='#2b2b2b')
        
        text_widget = scrolledtext.ScrolledText(
            help_window,
            bg='#1e1e1e',
            fg='#ffffff',
            font=("Consolas", 10),
            wrap=tk.WORD,
            padx=20,
            pady=20
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)
        
        close_btn = tk.Button(
            help_window,
            text="Close",
            command=help_window.destroy,
            bg='#00ff88',
            fg='#000000',
            font=("Arial", 11, "bold"),
            padx=30,
            pady=8
        )
        close_btn.pack(pady=10)

def main():
    """Main entry point"""
    root = tk.Tk()
    app = PTPDViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
