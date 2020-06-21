from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from app.models import User

BAD_VALIDATION = 'That {} is taken. Please choose a different one'


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(),
                    Length(min=3, max=25)]
    )

    email = StringField(
        'Email',
        validators=[DataRequired(),
                    Email()]
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired(),
                    EqualTo('confirm', message='Passwords must match')]
    )

    confirm = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError(BAD_VALIDATION.format('username'))

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError(BAD_VALIDATION.format('email'))


class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(),
                    Email()]
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )

    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RequestResetForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(),
                    Email()]
    )

    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first() is None:
            raise ValidationError('There is no account with that email. You must register first')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'New Password',
        validators=[DataRequired(),
                    EqualTo('confirm', message='Passwords must match')]
    )

    confirm = PasswordField(
        'Confirm New Password',
        validators=[DataRequired()]
    )

    submit = SubmitField('Reset Password')
