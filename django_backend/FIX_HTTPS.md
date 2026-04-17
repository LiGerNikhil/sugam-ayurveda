# HTTPS Setup Issue - Quick Fix

The SSL protocol error occurs because the certificate generation isn't working properly on your system.

## Easiest Solution - Use HTTP

For development, simply use HTTP instead of HTTPS:

```bash
python manage.py runserver
```

Then access your app at: **http://127.0.0.1:8000**

## Why This Works

- Your Django app is configured for development (DEBUG=True)
- HTTP works perfectly for local development
- No certificate issues
- No browser security warnings

## If You Absolutely Need HTTPS

### Option 1: Install Required Dependencies
```bash
pip install cryptography
python generate_cert.py
python start_https_simple.py
```

### Option 2: Use a Browser Extension
Install a browser extension that allows invalid certificates for localhost:
- Chrome: "Skip Certificate Error" extension
- Firefox: "Ignore Certificate Errors" extension

### Option 3: Use mkcert (Recommended)
1. Install mkcert: https://github.com/FiloSottile/mkcert
2. Run: `mkcert -install`
3. Run: `mkcert localhost 127.0.0.1`
4. Use the generated certificates

## Current Error Explained

```
ERR_SSL_PROTOCOL_ERROR
```

This means:
- The SSL handshake failed
- Certificate is invalid or missing
- Server isn't properly configured for HTTPS

## Recommendation

For development, **use HTTP**. It's simpler, faster, and works without any additional setup.

```bash
python manage.py runserver
# Access at: http://127.0.0.1:8000
```

HTTPS is only needed for production or when testing specific HTTPS features.
