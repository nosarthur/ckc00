#!/usr/bin/env python
import os
import json
from flask.ext.script import Manager
from datetime import datetime

from app import create_app
from app import db
from app.models import User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


@manager.command
def createDB(drop_first=False):
    ''' Create the database '''
    if drop_first:
        db.drop_all()
    db.create_all()


@manager.command
def adduser(email, user_id):
    '''Register a new user.'''
    from getpass import getpass
    password = getpass()
    password2 = getpass(prompt='confirm: ')
    if password != password2:
        import sys
        sys.exit('Error: passwords do not match.')
    db.create_all()
    user = User.query.filter_by(id=user_id).first()
    user.email = email
    user.password = password
    user.member_since = datetime.utcnow()
    db.session.commit()
    print('User {0} was registered successfully.'.format(user_id))


@manager.command
def createDBfromJSON():
    ''' Create DB from json file '''
    db.drop_all()
    db.create_all()
    with open('ckc00.json') as fin:
        users = json.load(fin)

    for user in users:
        user['username'] = user.get('username', user['id'])
        db.session.add(User(**user))

    db.session.commit()

if __name__ == '__main__':
    manager.run()
