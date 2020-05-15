import os
import secrets

from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required

from app import app, db, bcrypt
from app.forms import Registration, Login, UpdateProfile
from app.models import User, Post

posts = [
    {
        'autor': 'Aleksandr Tolstoy',
        'title': 'First blog post',
        'content': 'First post content',
        'date': 'April 22, 2020'

    },

    {
        'autor': 'Aleksey Redka',
        'title': 'Second blog post',
        'content': 'Second post content',
        'date': 'April 23, 2020'

    }
]


@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = Registration()
    if form.validate_on_submit():
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_pic) -> str:
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_pic.filename)
    pic_file = random_hex + file_ext
    pic_path = os.path.join(app.root_path, 'static/profile_pics', pic_file)
    form_pic.save(pic_path)
    return pic_file


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfile()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your profile has been updated', 'success')
        return redirect(url_for('profile'))  # PRG pattern
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('profile.html', title='Profile', image_file=image_file, form=form)
