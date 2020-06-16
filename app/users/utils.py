import os
import secrets
from functools import partial

from PIL import Image
from flask import url_for, current_app
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


def send_reset_email(user):
    token = user.reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made
'''
    mail.send(msg)
