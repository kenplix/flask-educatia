'''

Defines factory function in our Flask application.

Performs configuration from our settings class.

Author:     Aleksandr Tolstoy <aleksandr13tolstoy@gmail.com>
Created:    June, 2020
Modified:   -

'''

import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

from flask import Flask

from config import BaseConfig
from app.extensions import db, migrate, bcrypt, login_manager, mail, admin
from app.errors import error_templates
from app.admin import AdminView


def logger(app):
    '''
    Configures a file and mail handler for use with the Flask application's
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
        # Instantiates a new Mail Handler, sends internal server errors on
        # admin email specified by the app config.
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr=app.config['MAIL_USERNAME'] + '@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMIN_EMAIL'], subject='Educatia Failure',
            credentials=auth, secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        # Registers handler with the Flask pre-configured logger object.
        app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')

    # Instantiates a new File Handler, stores our log files in the directory
    # specified by the app config. Set the log level to the configured value.
    file_handler = RotatingFileHandler(
        app.config['LOGGING_LOCATION'],
        maxBytes=10240,
        backupCount=10
    )
    file_handler.setLevel(logging.INFO)
    # Creates and applies a log formatter, using the format specified
    # in the app config.
    file_handler.setFormatter(logging.Formatter(app.config['LOGGING_FORMAT']))
    # Registers handler with the Flask pre-configured logger object.
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Educatia startup')


def create_app(config_cls=BaseConfig):
    '''
    Creates a Flask application using the app factory pattern.

    Loads the configuration from class which contains in the 'config.py' file.

    :param config_cls: Sets configuration for the current application instance.
    :return:           Flask application instance
    '''

    app = Flask(__name__)
    app.config.from_object(config_cls)

    for ext in db, migrate, bcrypt, login_manager, mail, admin:
        ext.init_app(app)

    # Creates handlers for all necessary HTTP errors.
    error_templates(app)

    if not app.debug:
        logger(app)

    from app.models import User, Role, Post, Tag
    for model in User, Role, Post, Tag:
        admin.add_view(AdminView(model, db.session))

    from app.main.routes import main
    from app.auth.routes import auth
    from app.users.routes import users
    from app.posts.routes import posts
    for blueprint in auth, main, posts, users:
        app.register_blueprint(blueprint)

    return app
