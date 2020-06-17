import os
import secrets
from functools import partial

from PIL import Image
from flask import url_for, current_app, render_template
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


def create_message(header, template, recipients, **kwargs):
    return Message(
        header,
        sender=current_app.config['MAIL_USERNAME'],
        recipients=recipients,
        html=render_template(template, **kwargs)
    )


def send_token(user, header, template):
    token = user.generate_token()
    msg = create_message(
        header=header,
        template=template,
        recipients=[user.email],
        token=token
    )
    mail.send(msg)
