from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin

from config import BaseConfig
from app.admin import AdminView, HomeAdminView

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_message_category = 'info'
login_manager.login_view = 'users.login'
mail = Mail()
admin = Admin(
    url='/',
    name='Educatia',
    index_view=HomeAdminView()
)


def create_app(config_cls=BaseConfig):
    app = Flask(__name__)
    app.config.from_object(config_cls)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    admin.init_app(app)

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
    from app.users.routes import users
    from app.posts.routes import posts
    from app.errors.handlers import errors
    for blueprint in main, users, posts, errors:
        app.register_blueprint(blueprint)

    return app
