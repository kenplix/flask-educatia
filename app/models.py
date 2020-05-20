from datetime import datetime
from typing import Optional

from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def reset_token(self, expires_sec: int = 1800) -> str:
        ser = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return ser.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify(reset_token: str) -> Optional['User']:
        ser = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = ser.loads(reset_token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f'User <{self.username}: {self.email}>'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'Post <{self.date}: {self.title}>'
