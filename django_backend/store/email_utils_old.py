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

def generate_verification_token():
    """Generate a random verification token"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

def send_verification_email(user):
    """Send verification email with verification link"""
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    verification_url = f"http://127.0.0.1:8000/verify-email/{uid}/{token}/"
    
    subject = "Verify Your Email - Sugam Ayurveda"
    message = f"""
Hello {user.get_full_name() or user.username},

Thank you for registering with Sugam Ayurveda! 

Please click the link below to verify your email address and activate your account:

{verification_url}

This link will expire in 24 hours for security reasons.

If you didn't create an account with us, please ignore this email.

Best regards,
Sugam Ayurveda Team
"""
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
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
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        sender_email = settings.EMAIL_HOST_USER
        sender_password = 'kxkx hkrg ojfc byqq'  # App password
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = "Sugam Ayurveda - Email Verification OTP"
        message["From"] = f"Sugam Ayurveda <{sender_email}>"
        message["To"] = email
        
        # HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Email Verification</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    background: #f9fafb;
                    padding: 30px;
                    border-radius: 0 0 10px 10px;
                }}
                .otp-box {{
                    background: white;
                    border: 2px dashed #16a34a;
                    padding: 20px;
                    text-align: center;
                    margin: 20px 0;
                    border-radius: 10px;
                }}
                .otp-code {{
                    font-size: 36px;
                    font-weight: bold;
                    color: #16a34a;
                    letter-spacing: 5px;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    color: #6b7280;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Sugam Ayurveda</h1>
                <p>Email Verification</p>
            </div>
            
            <div class="content">
                <h2>Welcome to Sugam Ayurveda!</h2>
                <p>Thank you for registering with us. To complete your registration, please verify your email address using the OTP below:</p>
                
                <div class="otp-box">
                    <p>Your verification code is:</p>
                    <div class="otp-code">{otp}</div>
                    <p><small>This code will expire in 10 minutes</small></p>
                </div>
                
                <p><strong>Important:</strong></p>
                <ul>
                    <li>Never share this OTP with anyone</li>
                    <li>This OTP is valid for 10 minutes only</li>
                </ul>
            </div>
            
            <div class="footer">
                <p> 2026 Sugam Ayurveda. All rights reserved.</p>
                <p>Natural Ayurvedic Solutions for Better Health</p>
            </div>
        </body>
        </html>
        """
        
        # Attach HTML content
        message.attach(MIMEText(html_content, "html"))
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message.as_string())
        server.quit()
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def generate_otp():
    return str(random.randint(100000, 999999))

def store_otp(email, otp):
    cache_key = f"otp_{email}"
    cache.set(cache_key, otp, timeout=600)  # 10 minutes

def verify_otp(email, otp):
    cache_key = f"otp_{email}"
    stored_otp = cache.get(cache_key)
    if stored_otp and stored_otp == otp:
        cache.delete(cache_key)  # Clear OTP after verification
        return True
    return False
