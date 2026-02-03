import os 
import logging
from dotenv import load_dotenv

# Load .env file (development only)
load_dotenv()

class Config:

    # Database
    DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://localhost/kirikou_db')

    # Logging
    os.makedirs('logs', exist_ok=True)
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/kirikou.log')

    # Application 
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    APP_NAME = os.environ.get('APP_NAME', "Kirikou Media Intelligence")

    # RSS scraping
    FETCH_INTERVAL = int(os.environ.get('FETCH_INTERVAL', '3600'))
    REQUEST_TIMEOUT = int(os.environ.get('REQUEST_TIMEOUT', '10'))
    SECRET_KEY = os.environ.get('SECRET_KEY', 'NO_KEY')

    @classmethod
    def setup_logging(cls):
        logging.basicConfig(
            level = getattr(logging, cls.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(cls.LOG_FILE),
                logging.StreamHandler()
            ]
        )

    @classmethod
    def validate(cls):
        """Ensure required variables are set."""
        required = ['DATABASE_URL']
        missing = [var for var in required if not getattr(cls, var)]
        if missing:
            raise ValueError(f"Missing required env vars: {missing}") 
        
    




