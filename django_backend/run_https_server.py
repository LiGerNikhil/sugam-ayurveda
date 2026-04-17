#!/usr/bin/env python
"""
Simple HTTPS development server for Django
Usage: python run_https_server.py [port]
"""
import os
import sys
import ssl
import socket
import subprocess
from pathlib import Path

def generate_self_signed_cert(cert_file="localhost.pem", key_file="localhost-key.pem"):
    """Generate a self-signed SSL certificate using Python's ssl module"""
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
        import datetime
        
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        # Create certificate
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Django Development"),
            x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.DNSName("127.0.0.1"),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256())
        
        # Write certificate to file
        with open(cert_file, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        # Write private key to file
        with open(key_file, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        print(f"SSL certificates generated: {cert_file}, {key_file}")
        return True
        
    except ImportError:
        # Fallback to OpenSSL if cryptography is not available
        try:
            cmd = [
                'openssl', 'req', '-x509', '-newkey', 'rsa:2048',
                '-keyout', key_file, '-out', cert_file,
                '-days', '365', '-nodes',
                '-subj', '/C=US/ST=California/L=San Francisco/O=Django Development/CN=localhost'
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"SSL certificates generated: {cert_file}, {key_file}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Neither cryptography nor OpenSSL available: {e}")
            return False

def create_simple_https_server(port=8000):
    """Create a simple HTTPS server that proxies to Django"""
    cert_file = "localhost.pem"
    key_file = "localhost-key.pem"
    
    # Generate certificates if they don't exist
    if not os.path.exists(cert_file) or not os.path.exists(key_file):
        if not generate_self_signed_cert(cert_file, key_file):
            return False
    
    # Create a simple HTTPS server using Python's built-in modules
    server_script = f"""
import http.server
import ssl
import socketserver
import urllib.request
import os

class DjangoProxyHandler(http.server.SimpleHTTPRequestHandler):
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
            django_url = f'http://127.0.0.1:8001{{self.path}}'
            
            if self.command in ['POST', 'PUT']:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                req = urllib.request.Request(django_url, post_data)
            else:
                req = urllib.request.Request(django_url)
            
            # Copy headers
            for header, value in self.headers.items():
                if header.lower() not in ['host', 'connection']:
                    req.add_header(header, value)
            
            # Make request to Django
            with urllib.request.urlopen(req) as response:
                self.send_response(response.getcode())
                
                # Copy response headers
                for header, value in response.headers.items():
                    if header.lower() not in ['connection', 'transfer-encoding']:
                        self.send_header(header, value)
                self.end_headers()
                
                # Copy response body
                self.wfile.write(response.read())
                
        except Exception as e:
            self.send_error(500, f"Proxy error: {{str(e)}}")

# Start HTTPS server on port {port}
httpd = socketserver.TCPServer(('127.0.0.1', {port}), DjangoProxyHandler)

# Wrap socket with SSL
httpd.socket = ssl.wrap_socket(
    httpd.socket,
    certfile='{cert_file}',
    keyfile='{key_file}',
    server_side=True,
    ssl_version=ssl.PROTOCOL_TLS_SERVER,
)

print(f"HTTPS server running at https://127.0.0.1:{port}/")
print("Make sure Django is running on http://127.0.0.1:8001")
print("Press Ctrl+C to stop")

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\\nServer stopped")
    httpd.server_close()
"""
    
    # Write the server script
    with open("https_server.py", "w") as f:
        f.write(server_script)
    
    return True

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    
    print("Django HTTPS Development Server Setup")
    print("=" * 40)
    
    # Create HTTPS server
    if create_simple_https_server(port):
        print(f"\\nTo run your Django app with HTTPS:")
        print(f"1. Start Django on port 8001: python manage.py runserver 8001")
        print(f"2. Start HTTPS proxy: python https_server.py")
        print(f"3. Access your app at: https://127.0.0.1:{port}/")
        print(f"\\nNote: You'll see a browser security warning - this is normal for self-signed certificates.")
        print(f"Click 'Advanced' and 'Proceed to 127.0.0.1' to continue.")
    else:
        print("Failed to set up HTTPS server. Using regular HTTP instead.")
        print("Run: python manage.py runserver")
