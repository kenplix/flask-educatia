import os
import secrets
from threading import Thread
from functools import partial

from PIL import Image
from flask import current_app, render_template
from flask_login import current_user
from flask_mail import Message

from app import mail


def change_profile_picture(picture) -> str:
    picture_path = partial(
        os.path.join,
        current_app.root_path,
        'static/images/profile_pics'
    )
    if current_user.image_file != 'default.jpg':
        os.remove(picture_path(current_user.image_file))

    random_hex = secrets.token_hex(16)
    _, file_ext = os.path.splitext(picture.filename)
    picture_filename = random_hex + file_ext

    output_size = (125, 125)
    image = Image.open(picture)
    image.thumbnail(output_size)
    image.save(picture_path(picture_filename))
    return picture_filename


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_token(user, subject, template):
    app = current_app._get_current_object()
    msg = Message(
        subject,
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[user.email],
        html=render_template(template, token=user.generate_token())
    )
    Thread(target=send_async_email, args=(app, msg)).start()
