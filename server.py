#!/usr/bin/env python3
"""
Simple HTTP server for serving the D3.js Device Analytics Dashboard.
This server allows the HTML page to load CSV files via HTTP requests.
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom request handler to set proper CORS headers"""
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

def main():
    # Change to the project directory
    os.chdir(Path(__file__).parent)
    
    Handler = MyHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("=" * 60)
        print("🚀 Device Analytics Dashboard Server")
        print("=" * 60)
        print(f"\n✅ Server running at: http://localhost:{PORT}")
        print(f"📊 Dashboard URL: http://localhost:{PORT}/index.html")
        print("\n📌 Opening browser automatically...")
        print("\n⚠️  Press Ctrl+C to stop the server\n")
        print("=" * 60)
        
        # Open browser automatically
        try:
            webbrowser.open(f'http://localhost:{PORT}/index.html')
        except:
            print("⚠️  Could not open browser automatically. Please open the URL manually.")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✅ Server stopped.")
            print("=" * 60)

if __name__ == "__main__":
    main()

