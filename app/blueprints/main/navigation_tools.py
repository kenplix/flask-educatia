from app.models import Post


def paginate(page, posts, per_page=5):
    return posts.order_by(Post.date.desc()).paginate(page=page, per_page=per_page)


def search(posts, query: str):
    return posts.filter(Post.title.contains(query) | Post.content.contains(query))
