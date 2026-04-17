#!/usr/bin/env python
"""
Simple HTTPS starter for Django development
"""
import os
import sys
import subprocess
import threading
import time
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl

class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header('Location', f'https://127.0.0.1:8443{self.path}')
        self.end_headers()
    
    def do_POST(self):
        self.do_GET()
    
    def do_PUT(self):
        self.do_GET()
    
    def do_DELETE(self):
        self.do_GET()

def start_http_redirect():
    """Start HTTP server that redirects to HTTPS"""
    try:
        httpd = HTTPServer(('127.0.0.1', 8000), RedirectHandler)
        print("HTTP redirect server running on port 8000 -> https://127.0.0.1:8443")
        httpd.serve_forever()
    except Exception as e:
        print(f"HTTP redirect server failed: {e}")

def main():
    print("Django HTTPS Development Setup")
    print("=" * 40)
    
    # Check if certificates exist
    cert_files = ["localhost.pem", "localhost-key.pem"]
    if not all(os.path.exists(f) for f in cert_files):
        print("SSL certificates not found!")
        print("\nOption 1: Install cryptography and run:")
        print("  pip install cryptography")
        print("  python generate_cert.py")
        print("\nOption 2: Use regular HTTP server:")
        print("  python manage.py runserver")
        print("\nOption 3: Install OpenSSL and run:")
        print("  openssl req -x509 -newkey rsa:2048 -keyout localhost-key.pem -out localhost.pem -days 365 -nodes -subj '/CN=localhost'")
        return
    
    # Start Django on port 8001
    print("Starting Django on port 8001...")
    django_process = subprocess.Popen([
        sys.executable, "manage.py", "runserver", "8001"
    ])
    
    # Wait a moment for Django to start
    time.sleep(2)
    
    # Start HTTPS server on port 8443
    print("Starting HTTPS server on port 8443...")
    try:
        # Use Django's runserver with SSL if possible
        https_process = subprocess.Popen([
            sys.executable, "manage.py", "runserver", "8443",
            "--ssl-cert", "localhost.pem",
            "--ssl-key", "localhost-key.pem"
        ])
    except:
        print("Django SSL not supported, using proxy...")
        # Fall back to proxy method
        os.system(f"python simple_https.py 8443")
        return
    
    # Start HTTP redirect server in background
    redirect_thread = threading.Thread(target=start_http_redirect, daemon=True)
    redirect_thread.start()
    
    print("\nServers started!")
    print("HTTP (redirect): http://127.0.0.1:8000 -> https://127.0.0.1:8443")
    print("HTTPS: https://127.0.0.1:8443")
    print("Django (direct): http://127.0.0.1:8001")
    print("\nPress Ctrl+C to stop all servers")
    
    try:
        # Open browser
        webbrowser.open("https://127.0.0.1:8443")
        
        # Wait for processes
        django_process.wait()
        https_process.wait()
    except KeyboardInterrupt:
        print("\nStopping servers...")
        django_process.terminate()
        https_process.terminate()
        print("Servers stopped.")

if __name__ == "__main__":
    main()
