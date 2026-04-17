@echo off
echo Django HTTPS Development Server
echo ================================
echo.

echo Step 1: Starting Django on port 8001...
start "Django Server" cmd /k "python manage.py runserver 8001"

echo Step 2: Waiting 3 seconds for Django to start...
timeout /t 3 /nobreak >nul

echo Step 3: Starting HTTPS proxy on port 8000...
python run_https_server.py

pause
