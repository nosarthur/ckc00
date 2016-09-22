#!/usr/bin/env python
import os 
from flask.ext.script import Manager

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
def adduser(email, username):
    '''Register a new user.'''
    from getpass import getpass
    password = getpass()
    password2 = getpass(prompt='confirm: ')
    if password != password2:
        import sys
        sys.exit('Error: passwords do not match.')
    db.create_all()
    user = User(email=email, username=username, password=password)
    db.session.add(user)
    db.session.commit()
    print('User {0} was registered successfully.'.format(username))


if __name__ == '__main__':
    manager.run()

