'''

Creates the 'posts' blueprint, and define its endpoints.

Author:     Aleksandr Tolstoy <aleksandr13tolstoy@gmail.com>
Created:    June, 2020
Modified:   -

'''

from typing import Iterable

from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required

from .forms import PostForm
from ..main.navigation_tools import paginate
from app.extensions import db
from app.models import Post, Tag

posts = Blueprint('posts', __name__)


@posts.route('/posts/<int:post_id>')
def post(post_id: int):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/post.html', post=post, title=post.title)


@posts.route('/tags/<int:tag_id>')
def tag(tag_id: int):
    page = request.args.get('page', 1, type=int)
    tag = Tag.query.get_or_404(tag_id)
    return render_template('main/index.html', posts=paginate(page, tag.posts))


def make_tags(data: str, delimiter: str = ',') -> Iterable[Tag]:
    tags = map(lambda name: name.strip(), data.split(delimiter))
    for name in tags:
        if tag := Tag.query.filter_by(name=name).first():
            yield tag
        else:
            yield Tag(name=name)


@posts.route('/posts/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            author=current_user
        )
        tags = [tag for tag in make_tags(form.tags.data)]
        post.tags.extend(tags)

        db.session.add_all(tags)
        db.session.add(post)
        db.session.commit()
        flash('Your posts has been created', 'success')
        return redirect(url_for('main.home'))

    context = {
        'form': form,
        'title': 'New Post',
        'legend': 'New Post'
    }
    return render_template('posts/post_editor.html', **context)


@posts.route('/posts/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id: int):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.tags.clear()
        post.tags.extend(tag for tag in make_tags(form.tags.data))
        db.session.commit()
        flash('Your posts has been updated', 'success')
        return redirect(url_for('posts.post', post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.tags.data = ', '.join([tag.name for tag in post.tags])

    context = {
        'form': form,
        'title': 'Update Post',
        'legend': 'Update Post'
    }
    return render_template('posts/post_editor.html', **context)


@posts.route('/posts/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id: int):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your posts has been deleted', 'success')
    return redirect(url_for('main.home'))
