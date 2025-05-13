from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import bleach
import re
import logging
from config import Config
from monitoring import Monitoring
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize Flask-Mail
mail = Mail(app)

# Initialize rate limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
)

# Initialize monitoring
monitoring = Monitoring(app)

# Setup logging
logging.basicConfig(
    filename='form_submissions.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@app.route('/test-email', methods=['GET'])
def test_email():
    """Test route to verify email functionality"""
    try:
        msg = Message(
            'Test Email - The Causeway Estate',
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['RECIPIENT_EMAIL']]
        )
        msg.body = """
        This is a test email from The Causeway Estate website.
        If you receive this, the email system is working correctly.
        
        Time sent: {}
        """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        mail.send(msg)
        
        return jsonify({
            'message': 'Test email sent successfully',
            'recipient': app.config['RECIPIENT_EMAIL'],
            'status': 'success'
        }), 200
        
    except Exception as e:
        logging.error(f"Test email error: {str(e)}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/submit-form', methods=['POST'])
@limiter.limit("5 per minute")  # Rate limiting
def submit_form():
    try:
        data = request.get_json()
        
        # Required fields validation
        required_fields = ['name', 'email', 'message']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Sanitize inputs
        name = bleach.clean(data['name'])
        email = bleach.clean(data['email'])
        message = bleach.clean(data['message'])
        phone = bleach.clean(data.get('phone', 'Not provided'))
        
        # Create email message
        msg = Message(
            'New Contact Form Submission - The Causeway Estate',
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['RECIPIENT_EMAIL']]
        )
        
        # Email body
        msg.body = f"""
        New contact form submission from The Causeway Estate website:
        
        Name: {name}
        Email: {email}
        Phone: {phone}
        
        Message:
        {message}
        
        This is an automated message from your website contact form.
        """
        
        # Send email
        mail.send(msg)
        
        # Log successful submission
        monitoring.log_email_submission(email, 'success')
        
        return jsonify({
            'message': 'Thank you for your message. We will get back to you soon.',
            'status': 'success'
        }), 200
        
    except Exception as e:
        # Log error
        monitoring.log_email_submission(data.get('email', 'unknown'), f'error: {str(e)}')
        return jsonify({
            'error': 'An error occurred while processing your request. Please try again later.',
            'status': 'error'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify(monitoring.get_system_health()), 200

if __name__ == '__main__':
    app.run(debug=False) 