from datetime import datetime

from flask import (render_template, url_for, flash,
                   redirect, request, Blueprint)
from werkzeug.urls import url_parse
from flask_login import login_user, current_user, logout_user, login_required

from app import db
from app.models import User, Role, Post
from app.users.forms import (RegistrationForm, LoginForm, UpdateProfileForm,
                             RequestResetForm, ResetPasswordForm)
from app.users.utils import change_profile_picture, send_token

users = Blueprint('users', __name__)


@users.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.commit()


@users.route('/register', methods=['GET', 'POST'])
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
            header='Account Activation Request',
            template='mail/activate_account.html'
        )
        flash('An email has been send with instructions to activate your account', 'info')
        return redirect(url_for('users.login'))

    context = {
        'form': form,
        'title': 'Register'
    }
    return render_template('users/register.html', **context)


@users.route('/activate_account/<string:token>', methods=['GET', 'POST'])
def activate_account(token: str):
    user = User.verify_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.profile'))

    user.roles.append(Role.query.filter_by(name='Student').first())
    db.session.add(user)
    db.session.commit()
    flash(f'Your account has been activated', 'success')
    return redirect(url_for('users.login'))


@users.route('/login', methods=['GET', 'POST'])
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
                next_page = url_for('main.home')
            return redirect(next_page)
        flash('Login unsuccessful. Please check email and password', 'danger')

    context = {
        'form': form,
        'title': 'Login'
    }
    return render_template('users/login.html', **context)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_filename = change_profile_picture(form.picture.data)
            current_user.image_file = picture_filename
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your profile has been updated', 'success')
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for(
        'static',
        filename=f'images/profile_pics/{current_user.image_file}'
    )

    context = {
        'form': form,
        'title': 'Profile',
        'image_file': image_file
    }
    return render_template('users/profile.html', **context)


@users.route('/users/<string:username>')
def user_posts(username: str):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date.desc())\
        .paginate(page=page, per_page=5)
    return render_template('users/user_posts.html', user=user, posts=posts)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RequestResetForm()
    if form.validate_on_submit():
        send_token(
            user=User.query.filter_by(email=form.email.data).first(),
            header='Password Reset Request',
            template='mail/reset_password.html'
        )
        flash('An email has been send with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))

    context = {
        'form': form,
        'title': 'Reset Password'
    }
    return render_template('users/reset_request.html', **context)


@users.route('/reset_password/<string:token>', methods=['GET', 'POST'])
def reset_password(token: str):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash('Your password has been changed. You are now able to sign in', 'success')
        return redirect(url_for('users.login'))

    context = {
        'form': form,
        'title': 'Reset Password'
    }
    return render_template('users/reset_password.html', **context)
