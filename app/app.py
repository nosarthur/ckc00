#!/usr/bin/env python

from flask import Flask, render_template, request, redirect,  url_for, \
                  make_response, session
from flask_wtf import Form
from wtforms.fields import RadioField, SubmitField

from flask_sqlalchemy import SQLAlchemy

import hashlib
import hmac

from utils import do_query, do_name_query

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mySecret!' # use env var
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

@app.route('/', methods=['POST','GET'])
def index():
    x = hmac.new('nos','asdf').hexdigest()
    pageType = 'lala'

    resp = make_response(render_template('index.html'))
    resp.set_cookie('name', 'value', domain='nos.pythonanywhere.com')

    return resp

@app.route('/db2')
def name_query():
    name = request.args.get('name')

    if not name:
        return redirect(url_for('index'))
    header = 'id,bbs_id,city,state,latitude,longitude\n'
    return header + do_name_query(name)

@app.route('/db')
def class_query():
    sex = request.args.get('sex')
    class_type = request.args.get('class_type')

    if not sex or not class_type:
        return redirect(url_for('index'))

    header = 'id,bbs_id,city,state,latitude,longitude\n'
    return header + do_query(sex, class_type)

@app.route('/user/<name>', methods=['GET', 'POST'])
def user(name):
    return 'hello, {0}!'.format(name)
#    return render_template('signup.html', name=username)

if __name__ == '__main__':
    app.run(debug=True)
