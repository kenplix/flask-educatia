from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_message_category = 'info'
login_manager.login_view = 'users.login'
mail = Mail()
admin = Admin(name='Educatia')


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    admin.init_app(app)

    @app.cli.command()
    def createdb():
        db.create_all()

    from app.models import Role, Post, Tag
    for model in Role, Post, Tag:
        admin.add_view(ModelView(model, db.session))

    from app.main.routes import main
    from app.users.routes import users
    from app.posts.routes import posts
    from app.errors.handlers import errors
    for blueprint in main, users, posts, errors:
        app.register_blueprint(blueprint)

    return app
