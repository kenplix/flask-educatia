from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, InputRequired, Length, Email, EqualTo


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

# Issue: After bad input dont work EquealTo


class Login(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email()])
    password = PasswordField('Password',
                             validators=[InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
