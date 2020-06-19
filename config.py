import os

from dotenv import load_dotenv

# Load dotenv in the base root
APP_ROOT = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(APP_ROOT, '.env'))


class BaseConfig:
    """Set Flask configuration variables from .env file."""

    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = True

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URI',
        'sqlite:///' + os.path.join(APP_ROOT, 'site.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail SMTP server settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 25))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # Admin settings
    ADMIN_USERNAME = 'Admin'
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
