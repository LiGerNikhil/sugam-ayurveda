#!/usr/bin/env python
"""
Simple HTTPS server using Django's built-in development server
This creates a minimal HTTPS server without external dependencies
"""
import os
import sys
import ssl
import socket
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import urlopen, Request
from urllib.error import URLError

class DjangoProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.proxy_request()
    
    def do_POST(self):
        self.proxy_request()
    
    def do_PUT(self):
        self.proxy_request()
    
    def do_DELETE(self):
        self.proxy_request()
    
    def proxy_request(self):
        try:
            # Forward request to Django development server
            django_url = f'http://127.0.0.1:8001{self.path}'
            
            # Read request body for POST/PUT
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else None
            
            # Create request
            req = Request(django_url, post_data, method=self.command)
            
            # Copy headers
            for header, value in self.headers.items():
                if header.lower() not in ['host', 'connection']:
                    req.add_header(header, value)
            
            # Make request to Django
            with urlopen(req) as response:
                self.send_response(response.getcode())
                
                # Copy response headers
                for header, value in response.headers.items():
                    if header.lower() not in ['connection', 'transfer-encoding']:
                        self.send_header(header, value)
                self.end_headers()
                
                # Copy response body
                self.wfile.write(response.read())
                
        except Exception as e:
            self.send_error(500, f"Proxy error: {str(e)}")
            print(f"Proxy error: {e}")

def create_self_signed_cert():
    """Create a minimal self-signed certificate using built-in SSL"""
    cert_file = "localhost.pem"
    key_file = "localhost-key.pem"
    
    if os.path.exists(cert_file) and os.path.exists(key_file):
        return cert_file, key_file
    
    print("Generating self-signed certificate...")
    
    # Create a simple self-signed certificate
    from ssl import SSLContext, PROTOCOL_TLS_SERVER
    import subprocess
    
    # Try to generate with mkcert (if available)
    try:
        subprocess.run(['mkcert', 'localhost', '127.0.0.1'], check=True, capture_output=True)
        return 'localhost.pem', 'localhost-key.pem'
    except:
        pass
    
    # Try with OpenSSL
    try:
        cmd = [
            'openssl', 'req', '-x509', '-newkey', 'rsa:2048',
            '-keyout', key_file, '-out', cert_file,
            '-days', '365', '-nodes',
            '-subj', '/C=US/ST=California/L=San Francisco/O=Django Development/CN=localhost'
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return cert_file, key_file
    except:
        pass
    
    # If all else fails, create a dummy certificate
    print("Could not generate SSL certificate. Please install OpenSSL or mkcert.")
    print("For now, using HTTP instead...")
    return None, None

def start_https_server(port=8000):
    """Start HTTPS server"""
    cert_file, key_file = create_self_signed_cert()
    
    if not cert_file:
        print("Falling back to HTTP...")
        print(f"Access your app at: http://127.0.0.1:{port}")
        return False
    
    try:
        # Create HTTP server
        httpd = HTTPServer(('127.0.0.1', port), DjangoProxyHandler)
        
        # Wrap with SSL
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_file, key_file)
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        
        print(f"HTTPS server running at https://127.0.0.1:{port}/")
        print("Make sure Django is running on http://127.0.0.1:8001")
        print("Press Ctrl+C to stop")
        
        httpd.serve_forever()
        return True
        
    except Exception as e:
        print(f"Failed to start HTTPS server: {e}")
        return False

def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    
    print("Django HTTPS Development Server")
    print("=" * 40)
    
    if start_https_server(port):
        print(f"\nSuccess! Access your app at: https://127.0.0.1:{port}")
    else:
        print("\nHTTPS setup failed. Using HTTP instead.")
        print(f"Start Django with: python manage.py runserver {port}")

if __name__ == "__main__":
    main()
