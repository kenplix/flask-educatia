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
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(25),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    image_file = db.Column(
        db.String(20),
        nullable=False,
        default='default.jpg'
    )

    password = db.Column(
        db.String(60),
        nullable=False
    )

    posts = db.relationship(
        'Post',
        backref='author',
        lazy='dynamic'
    )

    def reset_token(self, expires_sec: int = 1800) -> str:
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify(reset_token: str) -> Optional['User']:
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(reset_token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f'User #{self.id} <{self.username}: {self.email}>'


PostTag = db.Table(
    'post_tag',

    db.Column(
        'post_id',
        db.Integer,
        db.ForeignKey('post.id')
    ),

    db.Column(
        'tag_id',
        db.Integer,
        db.ForeignKey('tag.id'))
)


class Post(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    tags = db.relationship(
        'Tag',
        secondary=PostTag,
        backref=db.backref('posts', lazy='dynamic'),
        lazy=True
    )

    def __repr__(self):
        return f'Post #{self.id} <{self.author.username}: {self.title}>'


class Tag(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    def __repr__(self):
        return f'Tag #{self.id} <{self.name}>'
