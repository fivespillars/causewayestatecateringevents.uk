import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Email Configuration
    MAIL_SERVER = 'smtp.gmail.com'  # For Gmail. Change if using different provider
    MAIL_PORT = 587  # TLS Port
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('EMAIL_USER')
    MAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    MAIL_MAX_EMAILS = 50  # Maximum emails to send in one connection
    MAIL_SUPPRESS_SEND = False  # Enable email sending
    
    # Recipient Email (where form submissions will be sent)
    RECIPIENT_EMAIL = 'elaijah@causewayestate.com'
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    
    # Rate Limiting
    RATELIMIT_DEFAULT = "5 per minute"
    RATELIMIT_STORAGE_URL = "memory://"
    
    # CORS Settings
    CORS_HEADERS = 'Content-Type'
    
    # Production Settings
    DEBUG = False
    TESTING = False
    PROPAGATE_EXCEPTIONS = True
    
    # Server Name (update when deploying)
    SERVER_NAME = os.getenv('SERVER_NAME', None)  # e.g., 'causewayestate.com' 