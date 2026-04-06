# Sugam Ayurveda - Django E-commerce Platform

A modern e-commerce platform for Ayurvedic products built with Django, featuring product management, customer orders, and seamless WhatsApp integration.

## 🌿 Features

- **Product Management**: Complete CRUD operations for Ayurvedic products
- **Category System**: Organized product categorization
- **Shopping Cart**: Add/remove products with quantity management
- **Order Management**: Customer order tracking and processing
- **User Authentication**: Registration, login, and email verification
- **WhatsApp Integration**: Direct customer support via WhatsApp
- **Responsive Design**: Mobile-friendly interface using Tailwind CSS
- **Admin Panel**: Django admin for content management
- **Email Notifications**: Professional HTML email templates
- **Image Management**: Product and category image uploads

## 🚀 Technology Stack

- **Backend**: Django 4.x
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Database**: SQLite (development)
- **Email**: Django Email Backend
- **Static Files**: WhiteNoise middleware
- **Deployment Ready**: Configured for production

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/sugam-ayurveda.git
   cd sugam-ayurveda
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env with your settings
   # DEBUG=False, SECRET_KEY=your-secret-key, etc.
   ```

5. **Database migration**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000` to access the application.

## 🌐 Production Deployment (VPS)

### Environment Variables
Set these environment variables in production:

```bash
export DEBUG=False
export SECRET_KEY='your-production-secret-key'
export ALLOWED_HOSTS='yourdomain.com,www.yourdomain.com'
export SITE_URL='https://yourdomain.com'
export USE_HTTPS=True
export EMAIL_HOST='smtp.yourprovider.com'
export EMAIL_PORT=587
export EMAIL_HOST_USER='your-email@example.com'
export EMAIL_HOST_PASSWORD='your-email-password'
```

### Using Gunicorn (Recommended)

1. **Install Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **Run with Gunicorn**
   ```bash
   gunicorn --bind 0.0.0.0:8000 sugam_ayurveda.wsgi:application
   ```

### Using Nginx + Gunicorn

1. **Install Nginx**
   ```bash
   sudo apt update
   sudo apt install nginx
   ```

2. **Create Nginx config** `/etc/nginx/sites-available/sugam-ayurveda`:
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com www.yourdomain.com;
       
       location = /favicon.ico { access_log off; log_not_found off; }
       location /static/ {
           root /path/to/your/project;
       }
       location /media/ {
           root /path/to/your/project;
       }
       location / {
           include proxy_params;
           proxy_pass http://unix:/run/gunicorn.sock;
       }
   }
   ```

3. **Enable site**
   ```bash
   sudo ln -s /etc/nginx/sites-available/sugam-ayurveda /etc/nginx/sites-enabled
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### Using Systemd Service

Create `/etc/systemd/system/gunicorn.service`:
```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/venv/bin/gunicorn --workers 3 --bind unix:/run/gunicorn.sock sugam_ayurveda.wsgi:application

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

## 📁 Project Structure

```
django_backend/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore             # Git ignore file
├── README.md              # This file
├── sugam_ayurveda/       # Main Django project
│   ├── settings.py        # Django settings
│   ├── urls.py          # URL configuration
│   └── wsgi.py         # WSGI configuration
├── store/               # Main Django app
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   ├── urls.py         # App URLs
│   ├── admin.py        # Admin configuration
│   ├── forms.py        # Django forms
│   └── email_utils.py  # Email utilities
├── templates/          # HTML templates
├── static/            # Static files (CSS, JS, images)
├── media/             # User uploaded files
└── staticfiles/       # Collected static files
```

## 🔧 Configuration

### Email Settings
Configure email in `settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

### WhatsApp Integration
Update WhatsApp number in templates:
```html
<a href="https://wa.me/916391251055">Chat on WhatsApp</a>
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and inquiries:
- **Email**: info@sugamayurveda.com
- **Phone**: +91 63912 51055
- **WhatsApp**: +91 63912 51055

## 🌟 Acknowledgments

- Django Framework for the robust backend
- Tailwind CSS for modern styling
- WhatsApp for customer communication
- All contributors and users of this platform
