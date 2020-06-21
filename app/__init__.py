import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin

from config import BaseConfig
from app.errors import error_templates
from app.admin import AdminView, HomeAdminView

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_message_category = 'info'
login_manager.login_view = 'auth.login'
mail = Mail()
admin = Admin(
    url='/',
    name='Educatia',
    index_view=HomeAdminView()
)


def logger(app):
    '''
    Configure a file and mail handler for use with the Flask application's
    built-in logger. The log location, log level, and log formats can all be
    configured via the config file. Note that this function mutates the
    provided 'app' parameter.
    :param app: Flask application instance
    '''
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] and app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])

        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        # Instantiate a new Mail Handler, sending internal server errors on
        # admin email specified by the app config.
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr=app.config['MAIL_USERNAME'] + '@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMIN_EMAIL'], subject='Educatia Failure',
            credentials=auth, secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        # Register our handler with the Flask object's pre-configured logger
        # object.
        app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')

    # Instantiate a new File Handler, storing our log files in the directory
    # specified by the app config. Set the log level to the configured value.
    file_handler = RotatingFileHandler(
        app.config['LOGGING_LOCATION'],
        maxBytes=10240,
        backupCount=10
    )
    file_handler.setLevel(logging.INFO)
    # Create a log formatter, using the format specified in the app config.
    # Apply this formatter to the above created handler.
    file_handler.setFormatter(logging.Formatter(app.config['LOGGING_FORMAT']))
    # Register our handler with the Flask object's pre-configured logger
    # object.
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Educatia startup')


def create_app(config_cls=BaseConfig):
    app = Flask(__name__)
    app.config.from_object(config_cls)

    for ext in db, migrate, bcrypt, login_manager, mail, admin:
        ext.init_app(app)

    if not app.debug:
        logger(app)

    # Create handlers for all necessary HTTP errors. In our case, we're simply
    # rendering templates for each error of interest.
    error_templates(app)

    @app.cli.command()
    def init_db():
        db.create_all()

    from app.models import User, Role, Post, Tag

    @app.cli.command()
    def create_roles():
        admin = Role(
            name='Admin',
            description='Site administrator'
        )
        tutor = Role(
            name='Tutor',
            description='Can all that can student plus creating and editing posts'
        )
        student = Role(
            name='Student',
            description='Can read posts, leave comments, send messages'
        )
        db.session.add_all((admin, tutor, student))
        db.session.commit()

    @app.cli.command()
    def create_admin():
        admin = User(
            username=app.config['ADMIN_USERNAME'],
            email=app.config['ADMIN_EMAIL'],
            password=app.config['ADMIN_PASSWORD']
        )
        db.session.add(admin)
        db.session.commit()
        admin.roles.append(Role.query.filter_by(name='Admin').first())
        db.session.add(admin)
        db.session.commit()

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Role': Role,
            'Post': Post,
            'Tag': Tag
        }

    for model in User, Role, Post, Tag:
        admin.add_view(AdminView(model, db.session))

    from app.main.routes import main
    from app.auth.routes import auth
    from app.users.routes import users
    from app.posts.routes import posts
    for blueprint in main, auth, users, posts:
        app.register_blueprint(blueprint)

    return app
