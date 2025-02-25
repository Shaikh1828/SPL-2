# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get email configuration from environment variables
EMAIL = os.getenv('EMAIL', 'your-app-email@gmail.com')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'your-app-password')

# JWT configuration
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_secret_key_should_be_strong_and_secure')
JWT_EXPIRATION = int(os.getenv('JWT_EXPIRATION', '5'))  # minutes