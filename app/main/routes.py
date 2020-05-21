from flask import render_template, request, Blueprint

from app.models import Post

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date.desc())\
        .paginate(page=page, per_page=5)
    return render_template('main/home.html', posts=posts)


@main.route('/about')
def about():
    return render_template('main/about.html', title='About')
