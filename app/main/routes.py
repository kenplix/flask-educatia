'''

Creates the 'main' blueprint, and define its endpoints.

Author:     Aleksandr Tolstoy <aleksandr13tolstoy@gmail.com>
Created:    June, 2020
Modified:   -

'''

from flask import render_template, request, Blueprint
from flask_login import current_user, login_required

from app.models import Post

main = Blueprint('main', __name__)


def paginate(page, posts, per_page=5):
    return posts.order_by(Post.date.desc()).paginate(page=page, per_page=per_page)


def search_filter(posts, query: str):
    return posts.filter(Post.title.contains(query) | Post.content.contains(query))


@main.route('/')
@main.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query
    if query := request.args.get('query'):
        posts = search_filter(posts, query)
    return render_template('main/index.html', posts=paginate(page, posts))


@main.route('/home')
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts()
    if query := request.args.get('query'):
        posts = search_filter(posts, query)
    return render_template('main/home.html', posts=paginate(page, posts))


@main.route('/about')
def about():
    return render_template('main/about.html', title='About')
