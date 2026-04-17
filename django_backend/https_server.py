
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
            django_url = f'http://127.0.0.1:8001{self.path}'
            
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
            self.send_error(500, f"Proxy error: {str(e)}")

# Start HTTPS server on port 8001
httpd = socketserver.TCPServer(('127.0.0.1', 8001), DjangoProxyHandler)

# Wrap socket with SSL
httpd.socket = ssl.wrap_socket(
    httpd.socket,
    certfile='localhost.pem',
    keyfile='localhost-key.pem',
    server_side=True,
    ssl_version=ssl.PROTOCOL_TLS_SERVER,
)

print(f"HTTPS server running at https://127.0.0.1:8001/")
print("Make sure Django is running on http://127.0.0.1:8001")
print("Press Ctrl+C to stop")

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped")
    httpd.server_close()
