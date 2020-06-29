'''

Defines application extensions to protect against recursive imports.

Author:     Aleksandr Tolstoy <aleksandr13tolstoy@gmail.com>
Created:    June, 2020
Modified:   -

'''

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin

from .admin import HomeAdminView

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

extensions = (
    db,
    migrate,
    bcrypt,
    login_manager,
    mail,
    admin
)
