from flask import render_template, url_for, flash, redirect

from app import app
from app.forms import Registration, Login
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
