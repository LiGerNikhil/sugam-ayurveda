from django.core.management.commands.runserver import Command as RunServerCommand
from django.core.servers.basehttp import get_internal_wsgi_application
from django.core.management import CommandError
import os
import sys
import ssl
import socket


class Command(RunServerCommand):
    help = "Starts a Django development server with HTTPS support"

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--certfile',
            default='localhost.pem',
            help='SSL certificate file (default: localhost.pem)'
        )
        parser.add_argument(
            '--keyfile', 
            default='localhost-key.pem',
            help='SSL private key file (default: localhost-key.pem)'
        )

    def handle(self, *args, **options):
        certfile = options['certfile']
        keyfile = options['keyfile']
        
        # Generate self-signed certificate if it doesn't exist
        if not os.path.exists(certfile) or not os.path.exists(keyfile):
            self.stdout.write(self.style.WARNING("SSL certificates not found. Generating self-signed certificates..."))
            try:
                self.generate_ssl_cert(certfile, keyfile)
                self.stdout.write(self.style.SUCCESS("SSL certificates generated successfully!"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to generate SSL certificates: {e}"))
                self.stdout.write(self.style.NOTICE("Please install OpenSSL or use: python manage.py runserver"))
                return

        # Override the server to use SSL
        from django.core.servers.basehttp import WSGIServer
        from wsgiref.simple_server import WSGIRequestHandler
        
        class HTTPSWSGIServer(WSGIServer):
            def server_bind(self):
                super().server_bind()
                self.socket = ssl.wrap_socket(
                    self.socket,
                    certfile=certfile,
                    keyfile=keyfile,
                    server_side=True,
                    ssl_version=ssl.PROTOCOL_TLS_SERVER,
                )

        # Monkey patch the WSGIServer
        import django.core.servers.basehttp
        django.core.servers.basehttp.WSGIServer = HTTPSWSGIServer
        
        self.stdout.write(self.style.SUCCESS(f"Starting HTTPS development server at https://127.0.0.1:{options['port']}/"))
        self.stdout.write(self.style.NOTICE("Quit the server with CTRL-C."))

        # Call the original runserver command
        super().handle(*args, **options)

    def generate_ssl_cert(self, certfile, keyfile):
        """Generate a self-signed SSL certificate"""
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
                    x509.IPAddress(socket.gethostbyname("127.0.0.1")),
                ]),
                critical=False,
            ).sign(private_key, hashes.SHA256())
            
            # Write certificate to file
            with open(certfile, "wb") as f:
                f.write(cert.public_bytes(serialization.Encoding.PEM))
            
            # Write private key to file
            with open(keyfile, "wb") as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))
                
        except ImportError:
            # Fallback to openssl command if cryptography is not available
            import subprocess
            subprocess.run([
                'openssl', 'req', '-x509', '-newkey', 'rsa:2048',
                '-keyout', keyfile, '-out', certfile,
                '-days', '365', '-nodes',
                '-subj', '/C=US/ST=California/L=San Francisco/O=Django Development/CN=localhost'
            ], check=True)
