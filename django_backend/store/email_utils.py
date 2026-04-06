import random
import string
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User
from django.urls import reverse

def generate_verification_token():
    """Generate a random verification token"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

def send_verification_email(user):
    """Send verification email with professional HTML template"""
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    # Dynamic URL generation
    from django.contrib.sites.shortcuts import get_current_site
    from django.templatetags.static import static
    try:
        site = get_current_site(None)
        domain = site.domain
        protocol = 'https' if hasattr(settings, 'USE_HTTPS') and settings.USE_HTTPS else 'http'
        base_url = f"{protocol}://{domain}"
    except:
        # Fallback to settings or default
        base_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
    
    verification_url = f"{base_url}/verify-email/{uid}/{token}/"
    
    # Get logo URL using Django's static tag
    logo_url = f"{base_url}{static('images/logo.png')}"
    
    subject = "Verify Your Email - Sugam Ayurveda"
    
    # Professional HTML email template
    html_message = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verify Your Email - Sugam Ayurveda</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }}
        .container {{
            max-width: 600px;
            margin: 20px auto;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #22c55e, #16a34a);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .logo {{
            max-width: 120px;
            height: auto;
            margin-bottom: 15px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
            font-weight: 600;
        }}
        .content {{
            padding: 40px 30px;
        }}
        .welcome {{
            font-size: 18px;
            color: #22c55e;
            font-weight: 600;
            margin-bottom: 20px;
        }}
        .message {{
            margin-bottom: 30px;
            color: #555;
        }}
        .verify-button {{
            display: inline-block;
            background: linear-gradient(135deg, #22c55e, #16a34a);
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            font-size: 16px;
            text-align: center;
            transition: transform 0.3s ease;
            margin: 20px 0;
        }}
        .verify-button:hover {{
            transform: translateY(-2px);
        }}
        .security-info {{
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 30px;
            text-align: center;
            color: #666;
            border-top: 1px solid #e9ecef;
        }}
        .footer p {{
            margin: 5px 0;
            font-size: 14px;
        }}
        .social-links {{
            margin: 20px 0;
        }}
        .social-links a {{
            margin: 0 10px;
            color: #22c55e;
            text-decoration: none;
        }}
        .alternative-link {{
            color: #6b7280;
            font-size: 12px;
            word-break: break-all;
            margin-top: 15px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            # <img src="{base_url}/static/images/logo.png" alt="Sugam Ayurveda Logo" class="logo" onerror="this.style.display='none'">
            <h1>Sugam Ayurveda</h1>
            <p>Traditional Healing, Modern Care</p>
        </div>
        
        <div class="content">
            <div class="welcome">
                Welcome, {user.get_full_name() or user.username}!
            </div>
            
            <div class="message">
                <p>Thank you for registering with Sugam Ayurveda! We're excited to have you join our community of wellness seekers.</p>
                <p>To complete your registration and activate your account, please verify your email address by clicking the button below:</p>
            </div>
            
            <a href="{verification_url}" class="verify-button">
                Verify Your Email Address
            </a>
            
            <div class="alternative-link">
                Or copy and paste this link into your browser:<br>
                {verification_url}
            </div>
            
            <div class="security-info">
                <strong>🔒 Security Notice:</strong> This verification link will expire in 24 hours for your security. If you didn't create an account with us, please ignore this email.
            </div>
            
            <div class="message">
                <p>If you have any questions or need assistance, feel free to contact our support team.</p>
                <p>We look forward to helping you on your wellness journey!</p>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>Sugam Ayurveda</strong></p>
            <p>Traditional Ayurvedic Products & Consultations</p>
            <p>📞 +91 63912 51055 | 📧 info@sugamayurveda.com</p>
            
            <div class="social-links">
                <a href="#">Facebook</a> | 
                <a href="#">Instagram</a> | 
                <a href="#">WhatsApp</a>
            </div>
            
            <p style="margin-top: 20px; font-size: 12px; color: #999;">
                © 2024 Sugam Ayurveda. All rights reserved.<br>
                This is an automated message, please do not reply to this email.
            </p>
        </div>
    </div>
</body>
</html>
"""
    
    # Plain text version for email clients that don't support HTML
    text_message = f"""
Hello {user.get_full_name() or user.username},

Thank you for registering with Sugam Ayurveda! 

Please click the link below to verify your email address and activate your account:

{verification_url}

This link will expire in 24 hours for security reasons.

If you didn't create an account with us, please ignore this email.

Best regards,
Sugam Ayurveda Team
📞 +91 63912 51055
📧 info@sugamayurveda.com
"""
    
    try:
        send_mail(
            subject,
            text_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def verify_email_token(uidb64, token):
    """Verify email token and return user if valid"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
        if default_token_generator.check_token(user, token):
            return user
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        pass
    
    return None

def activate_user_account(user):
    """Activate user account after email verification"""
    # Here you can add any additional logic for account activation
    # For now, we'll just return True since Django users are active by default
    return True
