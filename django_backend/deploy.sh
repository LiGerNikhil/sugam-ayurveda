#!/bin/bash

# Deployment Script for Sugam Ayurveda
# This script helps deploy the Django project to VPS

echo "🚀 Starting deployment of Sugam Ayurveda..."

# Exit on any error
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
print_status "Installing dependencies..."
pip install -r requirements.txt

# Install production dependencies
pip install gunicorn

# Environment setup
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating from template..."
    cp .env.example .env
    print_warning "Please edit .env file with your production settings!"
    exit 1
fi

# Database migrations
print_status "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
print_status "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if needed
print_status "Checking for superuser..."
python manage.py shell << EOF
from django.contrib.auth.models import User
if not User.objects.filter(is_superuser=True).exists():
    print("Creating superuser...")
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser created: admin/admin123")
else:
    print("Superuser already exists")
EOF

# Set permissions
print_status "Setting file permissions..."
chmod 755 manage.py
chmod -R 755 static/
chmod -R 755 media/

# Create Gunicorn socket directory
sudo mkdir -p /run/gunicorn
sudo chown www-data:www-data /run/gunicorn

# Setup systemd service
print_status "Setting up Gunicorn service..."
sudo tee /etc/systemd/system/gunicorn.service > /dev/null <<EOF
[Unit]
Description=gunicorn daemon for Sugam Ayurveda
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/venv/bin"
ExecStart=$(pwd)/venv/bin/gunicorn --workers 3 --bind unix:/run/gunicorn.sock sugam_ayurveda.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Setup Nginx configuration
print_status "Setting up Nginx configuration..."
read -p "Enter your domain name: " DOMAIN

sudo tee /etc/nginx/sites-available/sugam-ayurveda > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
    }
    
    location /static/ {
        root $(pwd);
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        root $(pwd);
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable Nginx site
sudo ln -sf /etc/nginx/sites-available/sugam-ayurveda /etc/nginx/sites-enabled/
sudo nginx -t

# Start services
print_status "Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
sudo systemctl restart nginx

# Check service status
print_status "Checking service status..."
sudo systemctl status gunicorn --no-pager
sudo systemctl status nginx --no-pager

print_status "🎉 Deployment completed successfully!"
print_status "Your site should be available at: http://$DOMAIN"
print_warning "Don't forget to:"
print_warning "1. Configure SSL certificate (Let's Encrypt recommended)"
print_warning "2. Update .env with production settings"
print_warning "3. Set up database backup"
print_warning "4. Configure firewall properly"
