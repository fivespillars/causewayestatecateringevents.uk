import os
import sys
import requests
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import logging

def check_environment():
    """Check if all required environment variables are set"""
    required_vars = ['EMAIL_USER', 'EMAIL_PASSWORD', 'SECRET_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing environment variables:", missing_vars)
        return False
    print("✅ Environment variables check passed")
    return True

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        'Flask', 'Flask-Mail', 'Flask-Limiter', 'python-dotenv',
        'bleach', 'gunicorn', 'Werkzeug', 'Flask-Cors',
        'sentry-sdk', 'prometheus-flask-exporter',
        'Flask-MonitoringDashboard', 'psutil'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_').split('[')[0])
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing packages:", missing_packages)
        return False
    print("✅ Dependencies check passed")
    return True

def check_email_config():
    """Test email configuration"""
    try:
        # Test SMTP connection
        smtp = smtplib.SMTP(os.getenv('MAIL_SERVER', 'smtp.gmail.com'), 587)
        smtp.starttls()
        smtp.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))
        smtp.quit()
        print("✅ Email configuration check passed")
        return True
    except Exception as e:
        print("❌ Email configuration error:", str(e))
        return False

def check_file_permissions():
    """Check if required directories and files are writable"""
    paths_to_check = [
        'logs',
        'logs/app_submissions.log',
        'logs/email_submissions.log',
        'dashboard.db'
    ]
    
    for path in paths_to_check:
        if os.path.exists(path):
            if not os.access(path, os.W_OK):
                print(f"❌ Permission error: {path} is not writable")
                return False
        else:
            try:
                if path.endswith('/'):
                    os.makedirs(path)
                else:
                    with open(path, 'a'):
                        pass
            except Exception as e:
                print(f"❌ Cannot create {path}: {str(e)}")
                return False
    
    print("✅ File permissions check passed")
    return True

def send_test_email():
    """Send a test email"""
    try:
        response = requests.get('http://localhost:5000/test-email')
        if response.status_code == 200:
            print("✅ Test email sent successfully")
            return True
        else:
            print("❌ Test email failed:", response.json())
            return False
    except Exception as e:
        print("❌ Test email error:", str(e))
        return False

def main():
    print("\n=== Deployment Checklist ===\n")
    
    checks = [
        check_environment(),
        check_dependencies(),
        check_email_config(),
        check_file_permissions(),
        send_test_email()
    ]
    
    print("\n=== Summary ===")
    if all(checks):
        print("\n✅ All checks passed! Ready for deployment!")
        return 0
    else:
        print("\n❌ Some checks failed. Please fix the issues before deploying.")
        return 1

if __name__ == "__main__":
    load_dotenv()
    sys.exit(main()) 