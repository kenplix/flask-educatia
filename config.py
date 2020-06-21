import os

from dotenv import load_dotenv

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))


class BaseConfig:
    """Flask configuration variables from .env file."""

    # Logging settings:
    LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s ' \
                     '[in %(pathname)s:%(lineno)d]'
    LOGGING_LOCATION = os.path.join(BASE_DIR, 'logs', 'app.log')

    # Flask settings:
    # Secret key for signing cookies
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # Statement for enabling the development environment
    DEBUG = False
    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2
    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True
    # Use a secure, unique and absolutely secret key for
    # signing the data.
    CSRF_SESSION_KEY = os.environ.get('CSRF_SESSION_KEY')

    # Flask-SQLAlchemy settings:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URI',
        'sqlite:///' + os.path.join(BASE_DIR, 'site.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail SMTP server settings:
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 25))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # Admin settings:
    ADMIN_USERNAME = 'Admin'
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
