# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get email configuration from environment variables
EMAIL = os.getenv('EMAIL', 'bsse1438@iit.du.ac.bd')  # Default to the email in email_service.py
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'jieayuasoceffzxc')  # Default to the password in email_service.py

# JWT configuration
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_secret_key_should_be_strong_and_secure')
JWT_EXPIRATION = int(os.getenv('JWT_EXPIRATION', '5'))  # minutes