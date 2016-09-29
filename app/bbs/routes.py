from flask import render_template, current_app, request, \
                  redirect, url_for, flash
from flask.ext.login import login_user, logout_user, login_required

from . import bbs

from .. import db
from ..models import Post

@bbs.route('/', methods=['GET', 'POST'])
def index():
    posts = Post.query.all()
    return render_template('bbs/index.html', posts=posts)


