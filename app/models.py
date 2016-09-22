from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin

from . import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    bbs_id = db.Column(db.String)
    name = db.Column(db.String)
    sex = db.Column(db.String) 
    city = db.Column(db.String)
    state = db.Column(db.String)
    class_type = db.Column(db.String)
    class_id = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    username = db.Column(db.String(64), nullable=False, 
                         unique=True, index=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), nullable=False, 
                         unique=True, index=True)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    #last_login = db.Column(db.DateTime()) 
    awards = db.Column(db.Integer, nullable=False, default=0)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User(88id='%s', name='%s'>" % (self.bbs_id, self.name)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
