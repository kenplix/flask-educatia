'''

Defines application factory function.

Author:     Aleksandr Tolstoy <aleksandr13tolstoy@gmail.com>
Created:    June, 2020
Modified:   -

'''

import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

from flask import Flask

from config import BaseConfig
from .errors import error_templates
from .extensions import db, admin, extensions
from .commands import commands
from .models import models
from .blueprints import blueprints
from .admin import AdminView


def logger(app):
    '''
    Configures, a file and mail handler. Note that this function
    mutates the provided 'app' parameter.

    :param app: Flask application instance
    :return: None
    '''
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] and app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])

        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()

        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr=app.config['MAIL_USERNAME'] + '@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMIN_EMAIL'], subject='Educatia Failure',
            credentials=auth, secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')

    file_handler = RotatingFileHandler(
        app.config['LOGGING_LOCATION'],
        maxBytes=10240,
        backupCount=10
    )
    file_handler.setLevel(app.config['LOGGING_LEVEL'])
    file_handler.setFormatter(logging.Formatter(app.config['LOGGING_FORMAT']))

    app.logger.addHandler(file_handler)
    app.logger.setLevel(app.config['LOGGING_LEVEL'])
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

    error_templates(app)

    if not app.debug:
        logger(app)

    for extension in extensions:
        extension.init_app(app)

    for command in commands:
        app.cli.add_command(command)

    for model in models:
        admin.add_view(AdminView(model, db.session))

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    return app
