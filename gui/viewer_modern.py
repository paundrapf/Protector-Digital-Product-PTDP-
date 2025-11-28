"""
Modern Gen-Z Styled PTDP PDF Viewer
Built with CustomTkinter for sleek, modern UI
Features: Anti-Screenshot, Anti-Copy, In-App PDF Reading
"""

import sys
import os
from pathlib import Path
import json
import io
import tempfile
from datetime import datetime
from tkinter import filedialog, messagebox
import tkinter as tk

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import customtkinter as ctk
except ImportError:
    print("Installing CustomTkinter...")
    os.system(f"{sys.executable} -m pip install customtkinter")
    import customtkinter as ctk

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Installing PyMuPDF for PDF rendering...")
    os.system(f"{sys.executable} -m pip install pymupdf")
    import fitz

from PIL import Image, ImageTk

from core.reader import PTDPReader
from core.license import LicenseValidator
from core.hwid import HardwareID
from core.updater import AutoUpdater, CURRENT_VERSION
import config

# Set theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SecurePDFViewer(ctk.CTk):
    """Secure PDF Viewer with anti-screenshot and anti-copy protection"""
    
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title(f"PTDP Viewer v{CURRENT_VERSION} - Protected PDF Reader")
        self.geometry("1200x800")
        self.minsize(900, 600)
        
        # Color scheme
        self.PRIMARY = "#FF6B9D"
        self.SECONDARY = "#C371F6"
        self.DARK_BG = "#0a0e27"
        self.CARD_BG = "#1a1f3a"
        
        # PDF State
        self.current_file = None
        self.reader = None
        self.pdf_doc = None
        self.current_page = 0
        self.total_pages = 0
        self.zoom_level = 1.0
        self.is_unlocked = False
        self.license_key = None
        
        # Updater
        self.updater = AutoUpdater("Viewer", CURRENT_VERSION)
        
        # Build UI first
        self.setup_ui()
        
        # Anti-screenshot protection (Windows) - after window is created
        self.after(100, self.apply_screenshot_protection)
        
        # Disable keyboard shortcuts for copy
        self.bind_security_keys()
        
        # Check for updates
        self.after(2000, self.check_updates_background)
    
    def apply_screenshot_protection(self):
        """Apply anti-screenshot protection using Windows API"""
        try:
            if sys.platform == 'win32':
                import ctypes
                # Get window handle
                self.update_idletasks()
                hwnd = ctypes.windll.user32.GetForegroundWindow()
                # SetWindowDisplayAffinity - WDA_EXCLUDEFROMCAPTURE = 0x00000011
                result = ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, 0x00000011)
                if result:
                    print("Anti-screenshot protection enabled")
        except Exception as e:
            print(f"Screenshot protection not available: {e}")
    
    def bind_security_keys(self):
        """Disable copy/paste and screenshot shortcuts"""
        # Disable common copy shortcuts
        self.bind('<Control-c>', lambda e: "break")
        self.bind('<Control-C>', lambda e: "break")
        self.bind('<Control-v>', lambda e: "break")
        self.bind('<Control-V>', lambda e: "break")
        self.bind('<Control-a>', lambda e: "break")
        self.bind('<Control-A>', lambda e: "break")
        self.bind('<Control-s>', lambda e: "break")
        self.bind('<Control-S>', lambda e: "break")
        self.bind('<Control-p>', lambda e: "break")
        self.bind('<Control-P>', lambda e: "break")
        
        # Disable print screen
        self.bind('<Print>', lambda e: "break")
        self.bind('<Snapshot>', lambda e: "break")
        
        # Navigation keys
        self.bind('<Left>', lambda e: self.prev_page())
        self.bind('<Right>', lambda e: self.next_page())
        self.bind('<Home>', lambda e: self.go_to_page(0))
        self.bind('<End>', lambda e: self.go_to_page(self.total_pages - 1) if self.total_pages > 0 else None)
        
        # Zoom keys
        self.bind('<Control-plus>', lambda e: self.zoom_in())
        self.bind('<Control-minus>', lambda e: self.zoom_out())
        self.bind('<Control-equal>', lambda e: self.zoom_in())
        self.bind('<Control-0>', lambda e: self.zoom_reset())
    
    def setup_ui(self):
        """Create the modern secure UI"""
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color=self.DARK_BG)
        main_frame.pack(fill="both", expand=True)
        
        # Header
        self.create_header(main_frame)
        
        # Content area
        self.content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Welcome screen (shown initially)
        self.welcome_frame = self.create_welcome_screen(self.content_frame)
        self.welcome_frame.pack(fill="both", expand=True)
        
        # License validation screen (hidden)
        self.license_frame = self.create_license_screen(self.content_frame)
        
        # PDF viewer screen (hidden)
        self.viewer_frame = self.create_viewer_screen(self.content_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
    
    def create_header(self, parent):
        """Create header bar"""
        header = ctk.CTkFrame(parent, height=70, fg_color=self.CARD_BG)
        header.pack(fill="x", padx=20, pady=(20, 10))
        header.pack_propagate(False)
        
        # Logo
        logo_frame = ctk.CTkFrame(header, fg_color="transparent")
        logo_frame.pack(side="left", padx=20)
        
        ctk.CTkLabel(
            logo_frame,
            text="🔐 PTDP",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.PRIMARY
        ).pack(side="left")
        
        ctk.CTkLabel(
            logo_frame,
            text="  Secure PDF Reader",
            font=ctk.CTkFont(size=14),
            text_color="#8B92B2"
        ).pack(side="left")
        
        # Right buttons
        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.pack(side="right", padx=20)
        
        self.open_btn = ctk.CTkButton(
            btn_frame,
            text="📂 Open File",
            command=self.open_file,
            fg_color=self.PRIMARY,
            hover_color="#FF5088",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=36,
            corner_radius=18
        )
        self.open_btn.pack(side="left", padx=5)
        
        self.close_btn = ctk.CTkButton(
            btn_frame,
            text="✕ Close",
            command=self.close_file,
            fg_color="transparent",
            hover_color="#2a2f4a",
            border_width=2,
            border_color=self.PRIMARY,
            font=ctk.CTkFont(size=13),
            height=36,
            corner_radius=18,
            state="disabled"
        )
        self.close_btn.pack(side="left", padx=5)
    
    def create_welcome_screen(self, parent):
        """Create welcome screen"""
        frame = ctk.CTkFrame(parent, fg_color=self.CARD_BG, corner_radius=20)
        
        content = ctk.CTkFrame(frame, fg_color="transparent")
        content.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(content, text="📄", font=ctk.CTkFont(size=80)).pack(pady=(0, 20))
        ctk.CTkLabel(
            content,
            text="PTDP Secure Reader",
            font=ctk.CTkFont(size=32, weight="bold")
        ).pack(pady=(0, 10))
        ctk.CTkLabel(
            content,
            text="Protected PDF viewing with maximum security",
            font=ctk.CTkFont(size=16),
            text_color="#8B92B2"
        ).pack(pady=(0, 30))
        
        features = [
            "🔒 Military-grade AES-256 encryption",
            "🛡️ Anti-screenshot protection",
            "🚫 Copy-paste disabled",
            "📖 In-app secure reading"
        ]
        for f in features:
            ctk.CTkLabel(content, text=f, font=ctk.CTkFont(size=14), text_color="#B5BAD0").pack(pady=3)
        
        ctk.CTkButton(
            content,
            text="📂 Open Protected File",
            command=self.open_file,
            fg_color=self.PRIMARY,
            hover_color="#FF5088",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            width=250,
            corner_radius=25
        ).pack(pady=30)
        
        return frame
    
    def create_license_screen(self, parent):
        """Create license validation screen"""
        frame = ctk.CTkFrame(parent, fg_color=self.CARD_BG, corner_radius=20)
        
        content = ctk.CTkFrame(frame, fg_color="transparent")
        content.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(content, text="🎫", font=ctk.CTkFont(size=60)).pack(pady=(0, 20))
        ctk.CTkLabel(
            content,
            text="Enter License Key",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(pady=(0, 10))
        
        # File info
        self.license_file_label = ctk.CTkLabel(
            content,
            text="",
            font=ctk.CTkFont(size=14),
            text_color="#8B92B2"
        )
        self.license_file_label.pack(pady=(0, 20))
        
        # License entry
        self.license_entry = ctk.CTkEntry(
            content,
            placeholder_text="PRODUCT-HWID-EXPIRY-SIGNATURE",
            font=ctk.CTkFont(size=14),
            height=45,
            width=400,
            corner_radius=10
        )
        self.license_entry.pack(pady=(0, 15))
        
        ctk.CTkButton(
            content,
            text="🔓 Unlock & Read",
            command=self.validate_and_open,
            fg_color=self.SECONDARY,
            hover_color="#B365E6",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            width=200,
            corner_radius=22
        ).pack(pady=(0, 15))
        
        self.license_status = ctk.CTkLabel(
            content,
            text="",
            font=ctk.CTkFont(size=13)
        )
        self.license_status.pack()
        
        return frame
    
    def create_viewer_screen(self, parent):
        """Create PDF viewer screen"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        
        # Top toolbar
        toolbar = ctk.CTkFrame(frame, height=50, fg_color=self.CARD_BG, corner_radius=10)
        toolbar.pack(fill="x", pady=(0, 10))
        toolbar.pack_propagate(False)
        
        # Navigation controls
        nav_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        nav_frame.pack(side="left", padx=15)
        
        self.prev_btn = ctk.CTkButton(
            nav_frame, text="◀ Prev", width=70, height=35,
            command=self.prev_page, fg_color=self.CARD_BG,
            hover_color="#2a2f4a", corner_radius=8
        )
        self.prev_btn.pack(side="left", padx=2)
        
        self.page_label = ctk.CTkLabel(
            nav_frame, text="Page 1 / 1",
            font=ctk.CTkFont(size=13)
        )
        self.page_label.pack(side="left", padx=15)
        
        self.next_btn = ctk.CTkButton(
            nav_frame, text="Next ▶", width=70, height=35,
            command=self.next_page, fg_color=self.CARD_BG,
            hover_color="#2a2f4a", corner_radius=8
        )
        self.next_btn.pack(side="left", padx=2)
        
        # Go to page
        ctk.CTkLabel(nav_frame, text="  Go to:", font=ctk.CTkFont(size=12)).pack(side="left", padx=(20, 5))
        self.page_entry = ctk.CTkEntry(nav_frame, width=60, height=30)
        self.page_entry.pack(side="left")
        self.page_entry.bind('<Return>', lambda e: self.go_to_page_from_entry())
        
        ctk.CTkButton(
            nav_frame, text="Go", width=40, height=30,
            command=self.go_to_page_from_entry,
            fg_color=self.PRIMARY, hover_color="#FF5088", corner_radius=5
        ).pack(side="left", padx=5)
        
        # Zoom controls
        zoom_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        zoom_frame.pack(side="right", padx=15)
        
        ctk.CTkButton(
            zoom_frame, text="−", width=35, height=35,
            command=self.zoom_out, fg_color=self.CARD_BG,
            hover_color="#2a2f4a", corner_radius=8,
            font=ctk.CTkFont(size=18)
        ).pack(side="left", padx=2)
        
        self.zoom_label = ctk.CTkLabel(
            zoom_frame, text="100%",
            font=ctk.CTkFont(size=13), width=60
        )
        self.zoom_label.pack(side="left", padx=5)
        
        ctk.CTkButton(
            zoom_frame, text="+", width=35, height=35,
            command=self.zoom_in, fg_color=self.CARD_BG,
            hover_color="#2a2f4a", corner_radius=8,
            font=ctk.CTkFont(size=18)
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            zoom_frame, text="Reset", width=55, height=30,
            command=self.zoom_reset, fg_color=self.SECONDARY,
            hover_color="#B365E6", corner_radius=5
        ).pack(side="left", padx=(10, 0))
        
        # PDF Canvas with scrollbar
        canvas_frame = ctk.CTkFrame(frame, fg_color=self.CARD_BG, corner_radius=15)
        canvas_frame.pack(fill="both", expand=True)
        
        # Canvas for PDF rendering
        self.pdf_canvas = tk.Canvas(
            canvas_frame,
            bg="#1a1f3a",
            highlightthickness=0,
            cursor="arrow"
        )
        self.pdf_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Vertical scrollbar
        self.v_scrollbar = ctk.CTkScrollbar(canvas_frame, command=self.pdf_canvas.yview)
        self.v_scrollbar.pack(side="right", fill="y", pady=10)
        self.pdf_canvas.configure(yscrollcommand=self.v_scrollbar.set)
        
        # Mouse wheel scroll
        self.pdf_canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.pdf_canvas.bind("<Button-4>", lambda e: self.pdf_canvas.yview_scroll(-1, "units"))
        self.pdf_canvas.bind("<Button-5>", lambda e: self.pdf_canvas.yview_scroll(1, "units"))
        
        # Disable right-click context menu
        self.pdf_canvas.bind("<Button-3>", lambda e: "break")
        
        return frame
    
    def create_status_bar(self, parent):
        """Create status bar"""
        status = ctk.CTkFrame(parent, height=35, fg_color=self.CARD_BG)
        status.pack(fill="x", padx=20, pady=(5, 15))
        status.pack_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            status, text="🔒 Secure Reader Ready",
            font=ctk.CTkFont(size=11), text_color="#8B92B2"
        )
        self.status_label.pack(side="left", padx=15)
        
        hwid = HardwareID.get_simple_hwid()
        ctk.CTkLabel(
            status, text=f"💻 {hwid[:16]}...",
            font=ctk.CTkFont(size=11), text_color="#8B92B2"
        ).pack(side="right", padx=15)
    
    def open_file(self):
        """Open protected file"""
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
            
            # Show license screen
            self.welcome_frame.pack_forget()
            self.viewer_frame.pack_forget()
            self.license_frame.pack(fill="both", expand=True)
            
            self.license_file_label.configure(
                text=f"📄 {os.path.basename(file_path)} ({metadata.get('product_id', 'Unknown')})"
            )
            self.license_entry.delete(0, "end")
            self.license_status.configure(text="")
            self.close_btn.configure(state="normal")
            
            self.update_status(f"Loaded: {os.path.basename(file_path)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file:\n{str(e)}")
    
    def validate_and_open(self):
        """Validate license and open PDF"""
        license_key = self.license_entry.get().strip()
        if not license_key:
            self.license_status.configure(text="Please enter license key", text_color="#F87171")
            return
        
        try:
            metadata = self.reader.read_metadata(self.current_file)
            product_id = metadata.get("product_id", "")
            
            validator = LicenseValidator()
            is_valid, message = validator.validate_offline(license_key, product_id)
            
            if is_valid:
                self.license_key = license_key
                self.is_unlocked = True
                self.license_status.configure(text="Valid! Loading PDF...", text_color="#4ADE80")
                
                # Load and display PDF
                self.after(300, self.load_pdf)
            else:
                self.license_status.configure(text=message, text_color="#F87171")
                
        except Exception as e:
            self.license_status.configure(text=f"Error: {str(e)}", text_color="#F87171")
    
    def load_pdf(self):
        """Load and decrypt PDF for viewing"""
        try:
            # Decrypt to memory
            result = self.reader.decrypt_file(self.current_file, self.license_key)
            
            if isinstance(result, dict):
                if result.get('success'):
                    pdf_data = result.get('content')
                else:
                    raise Exception(result.get('error', 'Decryption failed'))
            else:
                pdf_data = result
            
            # Load PDF with PyMuPDF
            self.pdf_doc = fitz.open(stream=pdf_data, filetype="pdf")
            self.total_pages = len(self.pdf_doc)
            self.current_page = 0
            self.zoom_level = 1.0
            
            # Switch to viewer
            self.license_frame.pack_forget()
            self.viewer_frame.pack(fill="both", expand=True)
            
            # Render first page
            self.after(100, self.render_page)
            
            self.update_status(f"📖 Reading: {os.path.basename(self.current_file)} | {self.total_pages} pages | 🔒 Protected")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load PDF:\n{str(e)}")
            self.license_status.configure(text=f"Load error: {str(e)}", text_color="#F87171")
    
    def render_page(self):
        """Render current page to canvas"""
        if not self.pdf_doc or self.current_page >= self.total_pages:
            return
        
        try:
            page = self.pdf_doc[self.current_page]
            
            # Apply zoom
            mat = fitz.Matrix(self.zoom_level * 1.5, self.zoom_level * 1.5)
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Convert to PhotoImage
            self.current_image = ImageTk.PhotoImage(img)
            
            # Clear canvas and display
            self.pdf_canvas.delete("all")
            
            # Center the image
            self.pdf_canvas.update_idletasks()
            canvas_width = self.pdf_canvas.winfo_width()
            x_offset = max(10, (canvas_width - pix.width) // 2)
            
            self.pdf_canvas.create_image(x_offset, 10, anchor="nw", image=self.current_image)
            
            # Update scroll region
            self.pdf_canvas.configure(scrollregion=(0, 0, max(canvas_width, pix.width + 20), pix.height + 20))
            
            # Update UI
            self.page_label.configure(text=f"Page {self.current_page + 1} / {self.total_pages}")
            self.zoom_label.configure(text=f"{int(self.zoom_level * 100)}%")
            self.page_entry.delete(0, "end")
            self.page_entry.insert(0, str(self.current_page + 1))
            
            # Update button states
            self.prev_btn.configure(state="normal" if self.current_page > 0 else "disabled")
            self.next_btn.configure(state="normal" if self.current_page < self.total_pages - 1 else "disabled")
            
        except Exception as e:
            print(f"Render error: {e}")
    
    def next_page(self):
        """Go to next page"""
        if self.pdf_doc and self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.render_page()
            self.pdf_canvas.yview_moveto(0)
    
    def prev_page(self):
        """Go to previous page"""
        if self.pdf_doc and self.current_page > 0:
            self.current_page -= 1
            self.render_page()
            self.pdf_canvas.yview_moveto(0)
    
    def go_to_page(self, page_num):
        """Go to specific page"""
        if self.pdf_doc and 0 <= page_num < self.total_pages:
            self.current_page = page_num
            self.render_page()
            self.pdf_canvas.yview_moveto(0)
    
    def go_to_page_from_entry(self):
        """Go to page from entry field"""
        try:
            page_num = int(self.page_entry.get()) - 1
            self.go_to_page(page_num)
        except ValueError:
            pass
    
    def zoom_in(self):
        """Zoom in"""
        if self.pdf_doc and self.zoom_level < 3.0:
            self.zoom_level += 0.25
            self.render_page()
    
    def zoom_out(self):
        """Zoom out"""
        if self.pdf_doc and self.zoom_level > 0.5:
            self.zoom_level -= 0.25
            self.render_page()
    
    def zoom_reset(self):
        """Reset zoom to 100%"""
        if self.pdf_doc:
            self.zoom_level = 1.0
            self.render_page()
    
    def on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.pdf_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def close_file(self):
        """Close current file"""
        if self.pdf_doc:
            self.pdf_doc.close()
            self.pdf_doc = None
        
        self.current_file = None
        self.reader = None
        self.is_unlocked = False
        self.license_key = None
        self.current_page = 0
        self.total_pages = 0
        
        # Show welcome screen
        self.license_frame.pack_forget()
        self.viewer_frame.pack_forget()
        self.welcome_frame.pack(fill="both", expand=True)
        
        self.close_btn.configure(state="disabled")
        self.update_status("🔒 Secure Reader Ready")
    
    def update_status(self, message):
        """Update status bar"""
        self.status_label.configure(text=message)
    
    def check_updates_background(self):
        """Check for updates"""
        self.updater.check_for_updates_async(self.on_update_check_complete)
    
    def on_update_check_complete(self, available, version, notes):
        """Handle update check result"""
        if available:
            self.after(0, lambda: self.show_update_dialog(version, notes))
    
    def show_update_dialog(self, version, notes):
        """Show update dialog"""
        result = messagebox.askyesno(
            "Update Available",
            f"New version v{version} available!\n\nCurrent: v{CURRENT_VERSION}\nNew: v{version}\n\nUpdate now?"
        )
        if result:
            self.download_and_apply_update()
    
    def download_and_apply_update(self):
        """Download and apply update"""
        import threading
        
        progress_win = ctk.CTkToplevel(self)
        progress_win.title("Updating...")
        progress_win.geometry("350x120")
        progress_win.transient(self)
        progress_win.grab_set()
        
        frame = ctk.CTkFrame(progress_win, fg_color=self.DARK_BG)
        frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        label = ctk.CTkLabel(frame, text="Downloading update...", font=ctk.CTkFont(size=14, weight="bold"))
        label.pack(pady=10)
        
        progress = ctk.CTkProgressBar(frame, width=280)
        progress.pack(pady=5)
        progress.set(0)
        
        def update_progress(downloaded, total):
            if total > 0:
                self.after(0, lambda: progress.set(downloaded / total))
        
        def do_download():
            path = self.updater.download_update(update_progress)
            if path and self.updater.apply_update(path):
                self.after(500, self.destroy)
            else:
                self.after(0, lambda: messagebox.showerror("Error", "Update failed"))
                self.after(0, progress_win.destroy)
        
        threading.Thread(target=do_download, daemon=True).start()


def main():
    """Launch secure viewer"""
    app = SecurePDFViewer()
    app.mainloop()


if __name__ == "__main__":
    main()
