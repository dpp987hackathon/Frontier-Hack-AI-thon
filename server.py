#!/usr/bin/env python3
"""
Simple HTTP Server for Device Analytics Dashboard
Serves files from the UI folder
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

# Configuration
PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to serve from project root"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def end_headers(self):
        # Enable CORS for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    # Check if UI directory exists
    if not os.path.exists("UI"):
        print(f"❌ Error: 'UI' directory not found!")
        print(f"   Please make sure the UI folder exists in {os.getcwd()}")
        sys.exit(1)
    
    # Check if index.html exists
    index_path = Path("UI") / "index.html"
    if not index_path.exists():
        print(f"❌ Error: index.html not found in UI!")
        sys.exit(1)
    
    # Check if data files exist
    data_path = Path("Data/Data Output")
    required_files = ["customer_data.csv", "device_data.csv", "nba_data.csv"]
    missing_files = []
    
    for file in required_files:
        if not (data_path / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("⚠️  Warning: Missing data files:")
        for file in missing_files:
            print(f"   - {file}")
        print(f"\n   Expected location: {data_path.absolute()}")
        print("\n   The dashboard may not load correctly without these files.")
        print("   Press Ctrl+C to stop, or wait 3 seconds to continue anyway...")
        
        import time
        time.sleep(3)
    
    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            url = f"http://localhost:{PORT}/UI/index.html"
            
            print("=" * 60)
            print("🚀 Device Analytics Dashboard Server")
            print("=" * 60)
            print(f"📂 Serving from: {os.path.abspath('.')}")
            print(f"🌐 Server running at: {url}")
            print(f"📊 Dashboard: {url}")
            print("\n✅ Server started successfully!")
            print("\n⏹️  Press Ctrl+C to stop the server")
            print("=" * 60)
            
            # Open browser
            print("\n🌐 Opening browser...")
            webbrowser.open(url)
            
            # Start serving
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        sys.exit(0)
    except OSError as e:
        if e.errno == 98 or e.errno == 10048:  # Address already in use
            print(f"\n❌ Error: Port {PORT} is already in use!")
            print(f"   Try using a different port or stop the other server.")
            print(f"\n   To use a different port, edit server.py and change PORT = {PORT}")
        else:
            print(f"\n❌ Error starting server: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
