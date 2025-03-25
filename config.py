import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Firebase Configuration
FIREBASE_DATABASE_URL = os.getenv('FIREBASE_DATABASE_URL')
FIREBASE_CREDENTIALS_FILE = os.getenv('FIREBASE_CREDENTIALS_FILE')

# Flask Configuration
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('FLASK_ENV') == 'development'
