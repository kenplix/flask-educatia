"""

Creates the 'auth' blueprint, and define its endpoints.

Author:     Aleksandr Tolstoy <aleksandr13tolstoy@gmail.com>
Created:    June, 2020
Modified:   -

"""

from threading import Thread

from flask_mail import Message
from flask import (render_template, current_app, url_for, flash,
                   redirect, request, Blueprint)
from werkzeug.urls import url_parse
from flask_login import login_user, current_user, logout_user

from .forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from app.extensions import db, mail
from app.models import User, Role

auth = Blueprint('auth', __name__)


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


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        send_token(
            user=user,
            subject='Account Activation Request',
            template='auth/activation_message.html'
        )
        flash('An email has been send with instructions to activate your account', 'info')
        return redirect(url_for('auth.login'))

    context = {
        'form': form,
        'title': 'Register'
    }
    return render_template('auth/register.html', **context)


@auth.route('/activate_account/<string:token>', methods=['GET', 'POST'])
def activate_account(token: str):
    user = User.verify_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('main.index'))

    user.roles.append(Role.query.filter_by(name='Student').first())
    db.session.add(user)
    db.session.commit()
    flash(f'Your account has been activated', 'success')
    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page is None or url_parse(next_page).netloc != '':
                next_page = url_for('main.index')
            return redirect(next_page)
        flash('Login unsuccessful. Please check email and password', 'danger')

    context = {
        'form': form,
        'title': 'Login'
    }
    return render_template('auth/login.html', **context)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/reset_request', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RequestResetForm()
    if form.validate_on_submit():
        send_token(
            user=User.query.filter_by(email=form.email.data).first(),
            subject='Password Reset Request',
            template='auth/reset_message.html'
        )
        flash('An email has been send with instructions to reset your password', 'info')
        return redirect(url_for('auth.login'))

    context = {
        'form': form,
        'title': 'Reset Password'
    }
    return render_template('auth/reset_request.html', **context)


@auth.route('/reset_password/<string:token>', methods=['GET', 'POST'])
def reset_password(token: str):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash('Your password has been changed. You are now able to sign in', 'success')
        return redirect(url_for('auth.login'))

    context = {
        'form': form,
        'title': 'Reset Password'
    }
    return render_template('auth/reset_password.html', **context)
