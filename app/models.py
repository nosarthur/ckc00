import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
from flask.ext.login import UserMixin

from . import db, login_manager

likes = db.Table('likes', 
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'),
                nullable=False),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'),
                nullable=False)
    )

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    bbs_id = db.Column(db.String)
    name = db.Column(db.String)
    sex = db.Column(db.String)
    city = db.Column(db.String(32))
    state = db.Column(db.String(32))
    class_type = db.Column(db.String)
    class_id = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    username = db.Column(db.String(64), index=True,
                         unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    site = db.Column(db.String(64))
    member_since = db.Column(db.DateTime())
    avatar_hash = db.Column(db.String(32), default='0')
    last_seen = db.Column(db.DateTime())
    awards = db.Column(db.Integer, nullable=False, default=0)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    liked = db.relationship('Post', secondary=likes, 
                backref=db.backref('fans', lazy='dynamic'), lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        if self.email and self.avatar_hash == '0':
            self.avatar_hash = \
                 hashlib.md5(self.email.encode('utf-8')).hexdigest()

        return '{url}/{hash}?s={size}&d={default}&r={rating}'\
            .format(url=url, hash=self.avatar_hash,
                    size=size, default=default,
                    rating=rating)

    def is_liking(self, post):
        return self.liked.filter(likes.c.post_id==post.id).count()>0

    def __repr__(self):
        return "<User(88id='%s', name='%s', email='%s')>" \
            % (self.bbs_id, self.name, self.email)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    likes = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return "<Post('%r', user_id='%s')>" % (self.body, self.user_id)



