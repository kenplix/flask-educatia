import os

from dotenv import load_dotenv

# Load dotenv in the base root
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
DOTENV_PATH = os.path.join(APP_ROOT, '.env')
load_dotenv(DOTENV_PATH)


class Config:
    """Set Flask configuration variables from .env file."""

    # General Flask Config
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = True

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
