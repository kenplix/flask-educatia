'''

Creates the 'users' blueprint, and define its endpoints.

Author:     Aleksandr Tolstoy <aleksandr13tolstoy@gmail.com>
Created:    June, 2020
Modified:   -

'''

import os
import secrets
from functools import partial
from datetime import datetime

from PIL import Image
from flask import (render_template, current_app, url_for, flash,
                   redirect, request, Blueprint)
from flask_login import current_user, login_required

from .forms import UpdateProfileForm, EmptyForm
from app.extensions import db
from app.models import User, Post

users = Blueprint('users', __name__)


@users.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.commit()


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


def image_file(user: User):
    return url_for(
        'static',
        filename=f'images/profile_pics/{user.image_file}'
    )


@users.route('/users/<string:username>')
def user(username: str):
    form = EmptyForm()
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f'User {username} not found', 'danger')
        return redirect(url_for('main.index'))
    if user == current_user:
        return redirect(url_for('users.profile'))

    context = {
        'form': form,
        'user': user,
        'image_file': image_file(user)
    }
    return render_template('users/user.html', **context)


@users.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_filename = change_profile_picture(form.picture.data)
            current_user.image_file = picture_filename
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your profile has been updated', 'success')
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.email.data = current_user.email

    context = {
        'form': form,
        'title': 'Profile',
        'image_file': image_file(current_user)
    }
    return render_template('users/profile.html', **context)


@users.route('/follow/<string:username>', methods=['GET', 'POST'])
@login_required
def follow(username: str):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        current_user.follow(user)
        db.session.commit()
        flash(f'You are following {username}', 'success')
        return redirect(url_for('users.user', username=username))
    else:
        return redirect(url_for('main.index'))


@users.route('/unfollow/<string:username>', methods=['GET', 'POST'])
@login_required
def unfollow(username: str):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You are not following {username}', 'success')
        return redirect(url_for('users.user', username=username))
    else:
        return redirect(url_for('main.index'))


@users.route('/users/<string:username>/posts')
def user_posts(username: str):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date.desc())\
        .paginate(page=page, per_page=5)
    return render_template('users/user_posts.html', user=user, posts=posts)
