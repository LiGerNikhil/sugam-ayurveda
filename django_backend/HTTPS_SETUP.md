# Django HTTPS Development Server Setup

This setup allows you to run your Django development server with HTTPS support.

## Quick Start

### Option 1: Use the Batch File (Windows)
1. Double-click `start_https.bat`
2. Wait for both servers to start
3. Open your browser and go to `https://127.0.0.1:8000`
4. Accept the security warning (click "Advanced" then "Proceed to 127.0.0.1")

### Option 2: Manual Setup

**Step 1: Start Django on port 8001**
```bash
python manage.py runserver 8001
```

**Step 2: In a new terminal, start the HTTPS proxy**
```bash
python run_https_server.py
```

**Step 3: Access your app**
Open your browser and go to `https://127.0.0.1:8000`

## What This Does

- Creates a self-signed SSL certificate for localhost
- Runs Django on port 8001 (HTTP)
- Creates an HTTPS proxy on port 8000 that forwards requests to Django
- Allows you to test HTTPS features during development

## Browser Security Warning

You will see a security warning like "Your connection is not private" - this is **normal** for self-signed certificates. Click "Advanced" and then "Proceed to 127.0.0.1" to continue.

## Alternative: Use HTTP

If you don't need HTTPS, simply run:
```bash
python manage.py runserver
```
And access your app at `http://127.0.0.1:8000`

## Troubleshooting

### If OpenSSL is not found:
1. Install OpenSSL from: https://slpweb.org/openssl/
2. Or use the regular HTTP server instead

### If port 8000 or 8001 is busy:
- Change the port in the commands
- Example: `python manage.py runserver 8002` and `python run_https_server.py 8001`

### Certificate Issues:
- Delete `localhost.pem` and `localhost-key.pem` files
- Run the setup again to generate new certificates

## Files Created
- `localhost.pem` - SSL certificate
- `localhost-key.pem` - SSL private key  
- `https_server.py` - HTTPS proxy server
- `start_https.bat` - Windows batch file for easy startup
