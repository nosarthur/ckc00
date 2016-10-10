#!/usr/bin/env python
import os
import imp
import json
from datetime import datetime
from flask_script import Manager
from migrate.versioning import api

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

    repo = app.config['SQLALCHEMY_MIGRATE_REPO']
    uri = app.config['SQLALCHEMY_DATABASE_URI']
    if not os.path.exists(repo):
        api.create(repo, 'database repository')
        api.version_control(uri, repo)
    else:
        api.version_control(uri, repo, api.version(repo))


@manager.command
def migrateDB():
    repo = app.config['SQLALCHEMY_MIGRATE_REPO']
    uri = app.config['SQLALCHEMY_DATABASE_URI']

    v = api.db_version(uri, repo)
    migration = repo + ('/versions/%03d_migration.py' % (v+1))
    tmp_module = imp.new_module('old_model')
    old_model = api.create_model(uri, repo)
    exec(old_model, tmp_module.__dict__)
    script = api.make_update_script_for_model(uri, repo, 
                                    tmp_module.meta, db.metadata)
    open(migration, "wt").write(script)
    api.upgrade(uri, repo)
    v = api.db_version(uri, repo)
    print('New migration saved as ' + migration)
    print('Current database version: ' + str(v))


@manager.command
def upgradeDB():
    repo = app.config['SQLALCHEMY_MIGRATE_REPO']
    uri = app.config['SQLALCHEMY_DATABASE_URI']
    api.upgrade(uri, repo)
    v = api.db_version(uri, repo)
    print('Current database version: ' + str(v))


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
    #user = User.query.filter_by(id=user_id).first()
    user = User.query.get(int(user_id))
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
        if user['bbs_id']:
            user['username'] = user.get('username', user['bbs_id'])
        else:
            user['username'] = user.get('username', user['id'])
        db.session.add(User(**user))

    db.session.commit()

if __name__ == '__main__':
    manager.run()
