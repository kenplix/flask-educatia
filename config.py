import os
import logging

from dotenv import load_dotenv

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))


class BaseConfig:
    """Flask configuration variables from .env file."""

    # Logging settings:
    LOGGING_LEVEL = logging.DEBUG
    LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s ' \
                     '[in %(pathname)s:%(lineno)d]'
    LOGGING_LOCATION = os.path.join(BASE_DIR, 'logs', 'app.log')

    # Flask settings:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = True
    THREADS_PER_PAGE = 2

    # Flask-SQLAlchemy settings:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URI',
        'sqlite:///' + os.path.join(BASE_DIR, 'site.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail SMTP server settings:
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # Flask-CKEditor settings:
    CKEDITOR_PKG_TYPE = 'full'

    # Admin settings:
    ADMIN_USERNAME = 'Admin'
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
