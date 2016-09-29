from flask import render_template, current_app, request, \
                  redirect, url_for, flash
from flask.ext.login import current_user

from . import bbs

from .. import db
from ..models import Post, likes

@bbs.route('/', methods=['GET', 'POST'])
def index():
    posts = Post.query.all()
    return render_template('bbs/index.html', posts=posts)


@bbs.route('/upvote/<post_id>')
def upvote(post_id):
    if not current_user.is_authenticated:
        flash('Registered user only.')
        return redirect(request.referrer)

    post = Post.query.get(int(post_id))
    if current_user.id == post.author.id:
        flash('Narcissism is destruction.')
        db.session.delete(post)
        db.session.commit()
        post.author.awards -= 1
        db.session.add(post.author)
        db.session.commit()
        return redirect(request.referrer)

    if current_user.is_liking(post):
        current_user.liked.remove(post)
        post.author.awards -= 1
        post.likes -= 1
    else:
        current_user.liked.append(post)
        post.author.awards += 1
        post.likes += 1

    db.session.add(post.author)
    db.session.add(post)
    db.session.commit()

    return redirect(request.referrer)
