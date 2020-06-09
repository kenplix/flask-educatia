from flask import render_template, request, Blueprint

from app.models import Post

main = Blueprint('main', __name__)


def paginate(page, posts, per_page=5):
    return posts.order_by(Post.date.desc()).paginate(page=page, per_page=per_page)


@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query
    if query := request.args.get('query'):
        posts = posts.filter(Post.title.contains(query) | Post.content.contains(query))
    return render_template('main/home.html', posts=paginate(page, posts))


@main.route('/about')
def about():
    return render_template('main/about.html', title='About')
