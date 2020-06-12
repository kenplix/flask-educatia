from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from app import db
from app.models import User, Post
from app.users.forms import (RegistrationForm, LoginForm, UpdateProfileForm,
                             RequestResetForm, ResetPasswordForm)
from app.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


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
        login_user(user)
        flash(f'Your account has been created', 'success')
        return redirect(url_for('main.home'))

    context = {
        'form': form,
        'title': 'Register'
    }
    return render_template('users/register.html', **context)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next = request.args.get('next')
            return redirect(next) if next else redirect(url_for('main.home'))
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
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your profile has been updated', 'success')
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static',
                         filename=f'profile_pics/{current_user.image_file}')
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
    return render_template('users/user_posts.html', user=users, posts=posts)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been send with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))

    context = {
        'form': form,
        'title': 'Reset Password'
    }
    return render_template('users/reset_request.html', **context)


@users.route('/reset_password/<string:token>', methods=['GET', 'POST'])
def reset_token(token: str):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify(token)
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
    return render_template('users/reset_token.html', **context)
