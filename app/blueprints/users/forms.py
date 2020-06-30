from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from flask_login import current_user

from app.models import User

BAD_VALIDATION = 'That {} is taken. Please choose a different one'


class UpdateProfileForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=3, max=25)
        ]
    )

    about_me = TextAreaField(
        'About me',
        validators=[Length(min=0, max=128)]
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    picture = FileField(
        'Update Profile Picture',
        validators=[FileAllowed(['jpg', 'png'])]
    )

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            if User.query.filter_by(username=username.data).first():
                raise ValidationError(BAD_VALIDATION.format('username'))

    def validate_email(self, email):
        if email.data != current_user.email:
            if User.query.filter_by(email=email.data).first():
                raise ValidationError(BAD_VALIDATION.format('email'))


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')
