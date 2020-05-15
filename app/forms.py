from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, InputRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user

from app.models import User


class Registration(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=3, max=25)])
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email()])
    password = PasswordField('Password',
                             validators=[InputRequired(),
                                         EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password', validators=[InputRequired()])
    submit = SubmitField('Sign Up')

    ERROR_MSG = 'That {} is taken. Please choose a different one'

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError(Registration.ERROR_MSG.format('username'))

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError(Registration.ERROR_MSG.format('email'))


class Login(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email()])
    password = PasswordField('Password',
                             validators=[InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class UpdateProfile(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=3, max=25)])
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email()])
    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')

    ERROR_MSG = 'That {} is taken. Please choose a different one'

    def validate_username(self, username):
        if username.data != current_user.username:
            if User.query.filter_by(username=username.data).first():
                raise ValidationError(Registration.ERROR_MSG.format('username'))

    def validate_email(self, email):
        if email.data != current_user.email:
            if User.query.filter_by(email=email.data).first():
                raise ValidationError(Registration.ERROR_MSG.format('email'))
