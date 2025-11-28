"""
Simple HTTP server for PTDP landing page
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import webbrowser
from pathlib import Path

class PTDPHandler(SimpleHTTPRequestHandler):
    """Custom handler with proper MIME types"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent), **kwargs)
    
    def end_headers(self):
        # Enable CORS for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()
    
    def log_message(self, format, *args):
        # Custom log format
        print(f"[PTDP Server] {format % args}")


def main():
    """Start the web server"""
    port = 8080
    server_address = ('', port)
    
    print("=" * 60)
    print("🚀 PTDP Landing Page Server")
    print("=" * 60)
    print(f"\n✓ Server starting on port {port}...")
    print(f"✓ URL: http://localhost:{port}")
    print(f"\n📂 Serving from: {Path(__file__).parent}")
    print("\n💡 Press Ctrl+C to stop the server\n")
    print("=" * 60 + "\n")
    
    # Start server
    httpd = HTTPServer(server_address, PTDPHandler)
    
    # Open in browser
    try:
        webbrowser.open(f'http://localhost:{port}')
        print("✓ Opening browser...\n")
    except:
        print("⚠ Could not open browser automatically")
        print(f"  Please visit: http://localhost:{port}\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print("👋 Server stopped")
        print("=" * 60)
        httpd.shutdown()


if __name__ == "__main__":
    main()
