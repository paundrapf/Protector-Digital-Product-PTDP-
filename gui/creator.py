# gui/creator.py
"""
PTDP Creator - Admin/Seller Tool
GUI untuk membuat protected .ptdp files
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sys
import os
import threading

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.creator import PTDPCreator
from core.license import LicenseValidator
from core.updater import AutoUpdater, CURRENT_VERSION

class PTDPCreatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"PTDP Creator v{CURRENT_VERSION} - Protect Your Digital Products")
        self.root.geometry("700x800")
        self.root.configure(bg='#2b2b2b')
        
        self.creator = PTDPCreator()
        self.updater = AutoUpdater("Creator", CURRENT_VERSION)
        
        self.setup_ui()
        
        # Check for updates after 2 seconds
        self.root.after(2000, self.check_updates_background)
    
    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg='#1e1e1e', height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="🔐 PTDP Creator",
            font=("Arial", 22, "bold"),
            bg='#1e1e1e',
            fg='#00ff88'
        ).pack(pady=25)
        
        # Main container
        main = tk.Frame(self.root, bg='#2b2b2b')
        main.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # File selection
        file_frame = tk.LabelFrame(
            main,
            text="  File to Protect  ",
            bg='#363636',
            fg='#00ff88',
            font=("Arial", 10, "bold"),
            padx=15,
            pady=15
        )
        file_frame.pack(fill=tk.X, pady=10)
        
        file_container = tk.Frame(file_frame, bg='#363636')
        file_container.pack(fill=tk.X)
        
        self.file_path_var = tk.StringVar()
        tk.Entry(
            file_container,
            textvariable=self.file_path_var,
            bg='#1e1e1e',
            fg='#ffffff',
            font=("Consolas", 10),
            state='readonly'
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        
        tk.Button(
            file_container,
            text="Browse",
            command=self.browse_file,
            bg='#4a4a4a',
            fg='#ffffff',
            font=("Arial", 10, "bold"),
            padx=15,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        # Product Details
        product_frame = tk.LabelFrame(
            main,
            text="  Product Information  ",
            bg='#363636',
            fg='#00ff88',
            font=("Arial", 10, "bold"),
            padx=15,
            pady=15
        )
        product_frame.pack(fill=tk.X, pady=10)
        
        # Product ID
        self.create_labeled_entry(product_frame, "Product ID:", "product_id")
        
        # Product Name
        self.create_labeled_entry(product_frame, "Product Name:", "product_name")
        
        # Master Password
        self.create_labeled_entry(product_frame, "Master Password:", "master_password", show="*")
        
        # Protection Options
        options_frame = tk.LabelFrame(
            main,
            text="  Protection Options  ",
            bg='#363636',
            fg='#00ff88',
            font=("Arial", 10, "bold"),
            padx=15,
            pady=15
        )
        options_frame.pack(fill=tk.X, pady=10)
        
        # Require Online
        self.require_online_var = tk.BooleanVar()
        tk.Checkbutton(
            options_frame,
            text="Require Online Validation",
            variable=self.require_online_var,
            bg='#363636',
            fg='#ffffff',
            selectcolor='#1e1e1e',
            activebackground='#363636',
            activeforeground='#00ff88',
            font=("Arial", 10)
        ).pack(anchor=tk.W, pady=5)
        
        # Max Devices
        device_container = tk.Frame(options_frame, bg='#363636')
        device_container.pack(fill=tk.X, pady=5)
        
        tk.Label(
            device_container,
            text="Max Devices:",
            bg='#363636',
            fg='#ffffff',
            font=("Arial", 10)
        ).pack(side=tk.LEFT)
        
        self.max_devices_var = tk.IntVar(value=1)
        tk.Spinbox(
            device_container,
            from_=1,
            to=10,
            textvariable=self.max_devices_var,
            bg='#1e1e1e',
            fg='#ffffff',
            font=("Arial", 10),
            width=10
        ).pack(side=tk.LEFT, padx=10)
        
        # Expiry Date
        expiry_container = tk.Frame(options_frame, bg='#363636')
        expiry_container.pack(fill=tk.X, pady=5)
        
        tk.Label(
            expiry_container,
            text="Expiry Date (YYYY-MM-DD):",
            bg='#363636',
            fg='#ffffff',
            font=("Arial", 10)
        ).pack(side=tk.LEFT)
        
        self.expiry_var = tk.StringVar()
        tk.Entry(
            expiry_container,
            textvariable=self.expiry_var,
            bg='#1e1e1e',
            fg='#ffffff',
            font=("Arial", 10),
            width=15
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Label(
            expiry_container,
            text="(leave empty for lifetime)",
            bg='#363636',
            fg='#888888',
            font=("Arial", 8)
        ).pack(side=tk.LEFT)
        
        # View Limit
        view_container = tk.Frame(options_frame, bg='#363636')
        view_container.pack(fill=tk.X, pady=5)
        
        tk.Label(
            view_container,
            text="View Limit:",
            bg='#363636',
            fg='#ffffff',
            font=("Arial", 10)
        ).pack(side=tk.LEFT)
        
        self.view_limit_var = tk.StringVar()
        tk.Entry(
            view_container,
            textvariable=self.view_limit_var,
            bg='#1e1e1e',
            fg='#ffffff',
            font=("Arial", 10),
            width=10
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Label(
            view_container,
            text="(leave empty for unlimited)",
            bg='#363636',
            fg='#888888',
            font=("Arial", 8)
        ).pack(side=tk.LEFT)
        
        # Create Button
        tk.Button(
            main,
            text="🔒 Create Protected File",
            command=self.create_protected,
            bg='#00ff88',
            fg='#000000',
            font=("Arial", 14, "bold"),
            padx=30,
            pady=15,
            cursor='hand2',
            relief=tk.FLAT
        ).pack(pady=30)
        
        # Status
        self.status_label = tk.Label(
            main,
            text="",
            bg='#2b2b2b',
            fg='#888888',
            font=("Arial", 9)
        )
        self.status_label.pack()
    
    def create_labeled_entry(self, parent, label_text, var_name, show=None):
        container = tk.Frame(parent, bg='#363636')
        container.pack(fill=tk.X, pady=8)
        
        tk.Label(
            container,
            text=label_text,
            bg='#363636',
            fg='#ffffff',
            font=("Arial", 10, "bold"),
            width=15,
            anchor=tk.W
        ).pack(side=tk.LEFT)
        
        entry_var = tk.StringVar()
        setattr(self, f"{var_name}_var", entry_var)
        
        tk.Entry(
            container,
            textvariable=entry_var,
            bg='#1e1e1e',
            fg='#ffffff',
            font=("Arial", 10),
            show=show
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select File to Protect",
            filetypes=[("All Files", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)
            
            # Auto-fill product name
            if not self.product_name_var.get():
                name = os.path.splitext(os.path.basename(file_path))[0]
                self.product_name_var.set(name)
    
    def create_protected(self):
        # Validate inputs
        if not self.file_path_var.get():
            messagebox.showwarning("Missing Info", "Please select a file to protect")
            return
        
        if not self.product_id_var.get():
            messagebox.showwarning("Missing Info", "Please enter Product ID")
            return
        
        if not self.master_password_var.get():
            messagebox.showwarning("Missing Info", "Please enter Master Password")
            return
        
        # Prepare config
        view_limit = self.view_limit_var.get()
        view_limit = int(view_limit) if view_limit else None
        
        expiry = self.expiry_var.get().strip()
        expiry = expiry if expiry else None
        
        config = {
            'product_id': self.product_id_var.get(),
            'product_name': self.product_name_var.get() or 'Digital Product',
            'master_password': self.master_password_var.get(),
            'require_online': self.require_online_var.get(),
            'max_devices': self.max_devices_var.get(),
            'expiry_date': expiry,
            'view_limit': view_limit,
            'version': '1.0',
            'license_type': 'premium'
        }
        
        # Output file
        input_file = self.file_path_var.get()
        output_file = os.path.splitext(input_file)[0] + '.ptdp'
        
        # Ask for output location
        output_file = filedialog.asksaveasfilename(
            title="Save Protected File As",
            defaultextension=".ptdp",
            initialfile=os.path.basename(output_file),
            filetypes=[("PTDP Files", "*.ptdp")]
        )
        
        if not output_file:
            return
        
        # Create protected file
        self.status_label.config(text="🔄 Creating protected file...", fg='#ffaa00')
        self.root.update()
        
        try:
            result = self.creator.create_protected_file(input_file, output_file, config)
            
            if result['success']:
                self.status_label.config(text="✅ Success!", fg='#00ff88')
                
                msg = f"""Protected file created successfully!

📁 File: {output_file}
🆔 Product ID: {result['product_id']}
📊 Size: {result['protected_size'] / 1024:.2f} KB

⚠️  IMPORTANT - Save this information:
   Master Password: {config['master_password']}
   Product ID: {result['product_id']}

You'll need these to generate license keys!

Do you want to generate a license key now?"""
                
                if messagebox.askyesno("Success!", msg):
                    self.generate_license_window(result['product_id'])
            else:
                self.status_label.config(text="❌ Failed!", fg='#ff6b35')
                messagebox.showerror("Error", result['error'])
        
        except Exception as e:
            self.status_label.config(text="❌ Error!", fg='#ff6b35')
            messagebox.showerror("Error", str(e))
    
    def generate_license_window(self, product_id):
        """Open license generation window"""
        from core.hwid import HardwareID
        
        win = tk.Toplevel(self.root)
        win.title("Generate License Key")
        win.geometry("500x400")
        win.configure(bg='#2b2b2b')
        
        tk.Label(
            win,
            text="Generate License Key",
            font=("Arial", 16, "bold"),
            bg='#2b2b2b',
            fg='#00ff88'
        ).pack(pady=20)
        
        # Product ID (readonly)
        frame1 = tk.Frame(win, bg='#2b2b2b')
        frame1.pack(fill=tk.X, padx=30, pady=10)
        tk.Label(frame1, text="Product ID:", bg='#2b2b2b', fg='#fff', width=15, anchor=tk.W).pack(side=tk.LEFT)
        tk.Entry(frame1, bg='#1e1e1e', fg='#fff', state='readonly', 
                textvariable=tk.StringVar(value=product_id)).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # HWID
        frame2 = tk.Frame(win, bg='#2b2b2b')
        frame2.pack(fill=tk.X, padx=30, pady=10)
        tk.Label(frame2, text="Device ID:", bg='#2b2b2b', fg='#fff', width=15, anchor=tk.W).pack(side=tk.LEFT)
        hwid_var = tk.StringVar()
        tk.Entry(frame2, textvariable=hwid_var, bg='#1e1e1e', fg='#fff').pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(
            win,
            text="(Leave empty for any device)",
            bg='#2b2b2b',
            fg='#888',
            font=("Arial", 8)
        ).pack()
        
        # Expiry
        frame3 = tk.Frame(win, bg='#2b2b2b')
        frame3.pack(fill=tk.X, padx=30, pady=10)
        tk.Label(frame3, text="Expiry (YYYYMMDD):", bg='#2b2b2b', fg='#fff', width=15, anchor=tk.W).pack(side=tk.LEFT)
        expiry_var = tk.StringVar(value="LIFETIME")
        tk.Entry(frame3, textvariable=expiry_var, bg='#1e1e1e', fg='#fff').pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Result
        result_text = tk.Text(win, height=4, bg='#1e1e1e', fg='#00ff88', font=("Consolas", 11))
        result_text.pack(fill=tk.X, padx=30, pady=20)
        
        def generate():
            hwid = hwid_var.get().strip() or None
            expiry = expiry_var.get().strip() or "LIFETIME"
            
            license = LicenseValidator.generate_license(
                product_id=product_id,
                hwid=hwid,
                expiry_date=expiry
            )
            
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"License Key:\n\n{license}")
            
            # Copy to clipboard
            win.clipboard_clear()
            win.clipboard_append(license)
            messagebox.showinfo("Generated!", f"License key generated and copied to clipboard!\n\n{license}")
        
        tk.Button(
            win,
            text="🔑 Generate License",
            command=generate,
            bg='#ff6b35',
            fg='#fff',
            font=("Arial", 12, "bold"),
            padx=30,
            pady=10
        ).pack(pady=10)
    
    def check_updates_background(self):
        """Check for updates in background"""
        self.updater.check_for_updates_async(self.on_update_check_complete)
    
    def on_update_check_complete(self, available, version, notes):
        """Called when update check is complete"""
        if available:
            self.root.after(0, lambda: self.show_update_dialog(version, notes))
    
    def show_update_dialog(self, version, notes):
        """Show update available dialog"""
        result = messagebox.askyesno(
            "Update Available",
            f"A new version (v{version}) is available!\n\n"
            f"Current: v{CURRENT_VERSION}\n"
            f"New: v{version}\n\n"
            f"Do you want to update now?"
        )
        
        if result:
            self.download_and_apply_update()
    
    def download_and_apply_update(self):
        """Download and apply the update"""
        # Create progress window
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Updating...")
        progress_window.geometry("400x150")
        progress_window.configure(bg='#2b2b2b')
        progress_window.transient(self.root)
        progress_window.grab_set()
        
        # Center window
        progress_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 400) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 150) // 2
        progress_window.geometry(f"+{x}+{y}")
        
        label = tk.Label(
            progress_window,
            text="Downloading update...",
            font=("Arial", 14, "bold"),
            bg='#2b2b2b',
            fg='#00ff88'
        )
        label.pack(pady=20)
        
        progress = ttk.Progressbar(progress_window, length=300, mode='determinate')
        progress.pack(pady=10)
        
        status_label = tk.Label(
            progress_window,
            text="0%",
            bg='#2b2b2b',
            fg='#ffffff'
        )
        status_label.pack()
        
        def update_progress(downloaded, total):
            if total > 0:
                percent = int((downloaded / total) * 100)
                self.root.after(0, lambda: progress.configure(value=percent))
                self.root.after(0, lambda: status_label.configure(
                    text=f"{percent}% ({downloaded // 1024 // 1024}MB / {total // 1024 // 1024}MB)"
                ))
        
        def do_download():
            update_path = self.updater.download_update(update_progress)
            if update_path:
                self.root.after(0, lambda: label.configure(text="Installing update..."))
                self.root.after(0, lambda: status_label.configure(text="Please wait..."))
                
                if self.updater.apply_update(update_path):
                    self.root.after(500, self.root.destroy)  # Close app for update
                else:
                    self.root.after(0, lambda: messagebox.showerror(
                        "Update Failed",
                        "Could not apply update. Please download manually from GitHub."
                    ))
                    self.root.after(0, progress_window.destroy)
            else:
                self.root.after(0, lambda: messagebox.showerror(
                    "Download Failed",
                    "Could not download update. Please try again later."
                ))
                self.root.after(0, progress_window.destroy)
        
        # Start download in background
        thread = threading.Thread(target=do_download)
        thread.daemon = True
        thread.start()

def main():
    root = tk.Tk()
    app = PTDPCreatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
