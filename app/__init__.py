from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt()
login_manager = LoginManager(app)
login_manager.login_message_category = 'info'
login_manager.login_view = 'users.login'
mail = Mail(app)

from app.main.routes import main
from app.users.routes import users
from app.posts.routes import posts
app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(posts)
