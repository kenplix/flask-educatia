#!../venv/bin/python
# -*- coding: UTF-8 -*-

from datetime import datetime

from flask import Flask, render_template, url_for, flash, redirect
from forms import Registration, Login
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '196e40bf26441892bd1b5ffc1093acfec6d55b73'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f'User({self.username}: {self.email} | {self.password})'

# TODO : create one to many relationship


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'Post({self.date}: {self.title})'


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
    form = Registration()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        # dummy data
        if form.email.data == 'alex@test.ua' \
                and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
