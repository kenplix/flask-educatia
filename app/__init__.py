from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin

from app.config import Config
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


def create_app(config_cls=Config):
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
    def create_admin():
        admin = User(
            username=app.config['ADMIN_USERNAME'],
            email=app.config['ADMIN_EMAIL'],
            password=app.config['ADMIN_PASSWORD']
        )
        role = Role(
            name='Admin',
            description='Site administrator'
        )
        db.session.add_all((admin, role))
        db.session.commit()
        admin.roles.append(role)
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
