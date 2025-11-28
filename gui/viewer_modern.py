"""
Modern Gen-Z Styled PTDP PDF Viewer
Built with CustomTkinter for sleek, modern UI
"""

import sys
import os
from pathlib import Path
import json
from datetime import datetime
from tkinter import filedialog, messagebox

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import customtkinter as ctk
except ImportError:
    print("Installing CustomTkinter for modern UI...")
    os.system(f"{sys.executable} -m pip install customtkinter")
    import customtkinter as ctk

from core.reader import PTDPReader
from core.license import LicenseValidator
from core.hwid import HardwareID
import config

# Set theme
ctk.set_appearance_mode("dark")  # Gen-Z loves dark mode
ctk.set_default_color_theme("blue")


class ModernPTDPViewer(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title("PTDP Viewer - Protected PDF Reader")
        self.geometry("1000x700")
        
        # Color scheme (matching website)
        self.PRIMARY = "#FF6B9D"
        self.SECONDARY = "#C371F6"
        self.DARK_BG = "#0a0e27"
        self.CARD_BG = "#1a1f3a"
        
        # State
        self.current_file = None
        self.reader = None
        
        # Build UI
        self.setup_ui()
        
    def setup_ui(self):
        """Create the modern UI"""
        
        # Main container with gradient effect
        main_frame = ctk.CTkFrame(self, fg_color=self.DARK_BG)
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Header
        self.create_header(main_frame)
        
        # Content area
        content = ctk.CTkFrame(main_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Welcome card (shown when no file is open)
        self.welcome_card = self.create_welcome_card(content)
        self.welcome_card.pack(fill="both", expand=True)
        
        # File info panel (hidden initially)
        self.info_panel = self.create_info_panel(content)
        
        # Status bar
        self.create_status_bar(main_frame)
        
    def create_header(self, parent):
        """Create modern header with gradient"""
        header = ctk.CTkFrame(parent, height=80, fg_color=self.CARD_BG)
        header.pack(fill="x", padx=20, pady=(20, 0))
        header.pack_propagate(False)
        
        # Logo/Title
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", padx=20)
        
        logo = ctk.CTkLabel(
            title_frame,
            text="🔐 PTDP",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.PRIMARY
        )
        logo.pack(side="left", padx=(0, 10))
        
        subtitle = ctk.CTkLabel(
            title_frame,
            text="Protected PDF Viewer",
            font=ctk.CTkFont(size=14),
            text_color="#8B92B2"
        )
        subtitle.pack(side="left")
        
        # Action buttons
        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.pack(side="right", padx=20)
        
        self.open_btn = ctk.CTkButton(
            btn_frame,
            text="📂 Open Protected File",
            command=self.open_file,
            fg_color=self.PRIMARY,
            hover_color="#FF5088",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            corner_radius=20
        )
        self.open_btn.pack(side="left", padx=5)
        
        self.close_btn = ctk.CTkButton(
            btn_frame,
            text="✕ Close",
            command=self.close_file,
            fg_color=self.CARD_BG,
            hover_color="#2a2f4a",
            border_width=2,
            border_color=self.PRIMARY,
            font=ctk.CTkFont(size=14),
            height=40,
            corner_radius=20,
            state="disabled"
        )
        self.close_btn.pack(side="left", padx=5)
        
    def create_welcome_card(self, parent):
        """Create welcome screen"""
        card = ctk.CTkFrame(parent, fg_color=self.CARD_BG, corner_radius=20)
        
        # Content
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.place(relx=0.5, rely=0.5, anchor="center")
        
        # Icon
        icon = ctk.CTkLabel(
            content,
            text="📄",
            font=ctk.CTkFont(size=80)
        )
        icon.pack(pady=(0, 20))
        
        # Title
        title = ctk.CTkLabel(
            content,
            text="Welcome to PTDP Viewer",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="white"
        )
        title.pack(pady=(0, 10))
        
        # Subtitle
        subtitle = ctk.CTkLabel(
            content,
            text="Your secure PDF protection solution",
            font=ctk.CTkFont(size=16),
            text_color="#8B92B2"
        )
        subtitle.pack(pady=(0, 30))
        
        # Instructions
        instructions = [
            "🔒 Protected files use military-grade encryption",
            "🎫 Enter your license key to unlock content",
            "💻 HWID-locked for maximum security",
            "⚡ Fast and lightweight viewer"
        ]
        
        for instruction in instructions:
            label = ctk.CTkLabel(
                content,
                text=instruction,
                font=ctk.CTkFont(size=14),
                text_color="#B5BAD0"
            )
            label.pack(pady=5)
        
        # Open button
        open_btn = ctk.CTkButton(
            content,
            text="📂 Open Protected File",
            command=self.open_file,
            fg_color=self.PRIMARY,
            hover_color="#FF5088",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            width=250,
            corner_radius=25
        )
        open_btn.pack(pady=30)
        
        return card
        
    def create_info_panel(self, parent):
        """Create file information panel"""
        panel = ctk.CTkFrame(parent, fg_color="transparent")
        
        # Left side - File details
        left_frame = ctk.CTkFrame(panel, fg_color=self.CARD_BG, corner_radius=20)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Title
        title = ctk.CTkLabel(
            left_frame,
            text="📋 File Information",
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w"
        )
        title.pack(fill="x", padx=20, pady=(20, 10))
        
        # Info frame
        self.info_labels = {}
        info_container = ctk.CTkFrame(left_frame, fg_color="transparent")
        info_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        info_items = [
            ("filename", "📄 Filename"),
            ("size", "💾 Size"),
            ("product", "🏷️ Product ID"),
            ("created", "📅 Protected On")
        ]
        
        for key, label in info_items:
            row = ctk.CTkFrame(info_container, fg_color="transparent")
            row.pack(fill="x", pady=8)
            
            label_widget = ctk.CTkLabel(
                row,
                text=label,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#8B92B2",
                anchor="w"
            )
            label_widget.pack(fill="x")
            
            value_widget = ctk.CTkLabel(
                row,
                text="—",
                font=ctk.CTkFont(size=14),
                text_color="white",
                anchor="w"
            )
            value_widget.pack(fill="x", pady=(5, 0))
            
            self.info_labels[key] = value_widget
        
        # Right side - License validation
        right_frame = ctk.CTkFrame(panel, fg_color=self.CARD_BG, corner_radius=20)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Title
        title = ctk.CTkLabel(
            right_frame,
            text="🎫 License Validation",
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w"
        )
        title.pack(fill="x", padx=20, pady=(20, 10))
        
        # License input
        input_container = ctk.CTkFrame(right_frame, fg_color="transparent")
        input_container.pack(fill="x", padx=20, pady=(0, 10))
        
        label = ctk.CTkLabel(
            input_container,
            text="Enter License Key:",
            font=ctk.CTkFont(size=13),
            text_color="#8B92B2",
            anchor="w"
        )
        label.pack(fill="x", pady=(0, 5))
        
        self.license_entry = ctk.CTkEntry(
            input_container,
            placeholder_text="PRODUCT-HWID-EXPIRY-SIGNATURE",
            font=ctk.CTkFont(size=14),
            height=40,
            corner_radius=10
        )
        self.license_entry.pack(fill="x", pady=(0, 10))
        
        self.validate_btn = ctk.CTkButton(
            input_container,
            text="✓ Validate & Unlock",
            command=self.validate_license,
            fg_color=self.SECONDARY,
            hover_color="#B365E6",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            corner_radius=20
        )
        self.validate_btn.pack(fill="x")
        
        # Status
        self.license_status = ctk.CTkLabel(
            right_frame,
            text="",
            font=ctk.CTkFont(size=13),
            anchor="w"
        )
        self.license_status.pack(fill="x", padx=20, pady=(10, 0))
        
        # Export button (disabled until validated)
        self.export_btn = ctk.CTkButton(
            right_frame,
            text="💾 Export PDF",
            command=self.export_file,
            fg_color=self.PRIMARY,
            hover_color="#FF5088",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            corner_radius=20,
            state="disabled"
        )
        self.export_btn.pack(fill="x", padx=20, pady=20)
        
        return panel
        
    def create_status_bar(self, parent):
        """Create bottom status bar"""
        status_bar = ctk.CTkFrame(parent, height=40, fg_color=self.CARD_BG)
        status_bar.pack(fill="x", padx=20, pady=(10, 20))
        status_bar.pack_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            status_bar,
            text="Ready to protect your digital products 🚀",
            font=ctk.CTkFont(size=12),
            text_color="#8B92B2"
        )
        self.status_label.pack(side="left", padx=20)
        
        # HWID display
        hwid = HardwareID.get_simple_hwid()
        hwid_label = ctk.CTkLabel(
            status_bar,
            text=f"💻 Device: {hwid[:16]}...",
            font=ctk.CTkFont(size=12),
            text_color="#8B92B2"
        )
        hwid_label.pack(side="right", padx=20)
        
    def open_file(self):
        """Open a protected file"""
        file_path = filedialog.askopenfilename(
            title="Select Protected File",
            filetypes=[("PTDP Files", "*.ptdp"), ("All Files", "*.*")]
        )
        
        if not file_path:
            return
            
        try:
            self.reader = PTDPReader()
            metadata = self.reader.read_metadata(file_path)
            
            self.current_file = file_path
            
            # Update UI
            self.welcome_card.pack_forget()
            self.info_panel.pack(fill="both", expand=True)
            self.close_btn.configure(state="normal")
            
            # Update file info
            self.info_labels["filename"].configure(text=os.path.basename(file_path))
            self.info_labels["size"].configure(text=f"{os.path.getsize(file_path) / 1024:.2f} KB")
            self.info_labels["product"].configure(text=metadata.get("product_id", "Unknown"))
            self.info_labels["created"].configure(text=metadata.get("created_date", "Unknown"))
            
            self.update_status(f"✓ Loaded: {os.path.basename(file_path)}", "success")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file:\n{str(e)}")
            self.update_status(f"✗ Error: {str(e)}", "error")
            
    def close_file(self):
        """Close current file"""
        self.current_file = None
        self.reader = None
        
        # Reset UI
        self.info_panel.pack_forget()
        self.welcome_card.pack(fill="both", expand=True)
        self.close_btn.configure(state="disabled")
        self.export_btn.configure(state="disabled")
        
        # Clear fields
        self.license_entry.delete(0, "end")
        self.license_status.configure(text="", text_color="white")
        
        for label in self.info_labels.values():
            label.configure(text="—")
            
        self.update_status("Ready to protect your digital products 🚀", "info")
        
    def validate_license(self):
        """Validate the license key"""
        if not self.current_file:
            messagebox.showwarning("No File", "Please open a protected file first")
            return
            
        license_key = self.license_entry.get().strip()
        if not license_key:
            messagebox.showwarning("No License", "Please enter a license key")
            return
            
        try:
            metadata = self.reader.read_metadata(self.current_file)
            product_id = metadata.get("product_id", "")
            
            validator = LicenseValidator()
            is_valid, message = validator.validate_offline(license_key, product_id)
            
            if is_valid:
                self.license_status.configure(
                    text="✓ " + message,
                    text_color="#4ADE80"
                )
                self.export_btn.configure(state="normal")
                self.update_status(f"✓ License validated successfully", "success")
            else:
                self.license_status.configure(
                    text="✗ " + message,
                    text_color="#F87171"
                )
                self.export_btn.configure(state="disabled")
                self.update_status(f"✗ License validation failed", "error")
                
        except Exception as e:
            messagebox.showerror("Validation Error", str(e))
            self.license_status.configure(
                text=f"✗ Error: {str(e)}",
                text_color="#F87171"
            )
            
    def export_file(self):
        """Export the decrypted PDF"""
        if not self.current_file:
            return
            
        license_key = self.license_entry.get().strip()
        if not license_key:
            messagebox.showwarning("No License", "Please validate license first")
            return
            
        # Choose save location
        original_name = os.path.basename(self.current_file).replace(".ptdp", ".pdf")
        save_path = filedialog.asksaveasfilename(
            title="Save Decrypted PDF",
            defaultextension=".pdf",
            initialfile=original_name,
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        
        if not save_path:
            return
            
        try:
            # Decrypt and save
            content = self.reader.decrypt_file(
                self.current_file,
                license_key=license_key
            )
            
            with open(save_path, 'wb') as f:
                f.write(content)
                
            messagebox.showinfo(
                "Success",
                f"PDF exported successfully!\n\nSaved to:\n{save_path}"
            )
            self.update_status(f"✓ Exported: {os.path.basename(save_path)}", "success")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export:\n{str(e)}")
            self.update_status(f"✗ Export failed: {str(e)}", "error")
            
    def update_status(self, message, status_type="info"):
        """Update status bar"""
        colors = {
            "info": "#8B92B2",
            "success": "#4ADE80",
            "error": "#F87171"
        }
        
        self.status_label.configure(
            text=message,
            text_color=colors.get(status_type, colors["info"])
        )


def main():
    """Launch the viewer"""
    app = ModernPTDPViewer()
    app.mainloop()


if __name__ == "__main__":
    main()
