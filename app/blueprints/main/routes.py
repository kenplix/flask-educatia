"""

Creates the 'main' blueprint, and define its endpoints.

Author:     Aleksandr Tolstoy <aleksandr13tolstoy@gmail.com>
Created:    June, 2020
Modified:   -

"""

from flask import render_template, request, Blueprint
from flask_login import current_user, login_required

from .navigation_tools import paginate, search
from app.models import Post

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query
    if query := request.args.get('query'):
        posts = search(posts, query)
    return render_template('main/index.html', posts=paginate(page, posts))


@main.route('/home')
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts()
    if query := request.args.get('query'):
        posts = search(posts, query)
    return render_template('main/home.html', posts=paginate(page, posts))


@main.route('/about')
def about():
    return render_template('main/about.html', title='About')
