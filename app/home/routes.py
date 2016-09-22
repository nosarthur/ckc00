from flask import render_template, flash, redirect, url_for, request
from flask.ext.login import login_required, current_user

from . import home
from .forms import ProfileForm, QueryForm
from .. import db
from ..models import User

from ..utils import do_query, do_name_query

@home.route('/', methods=['GET', 'POST'])
def index():
    form = QueryForm()
    if form.validate_on_submit():
        pass
    return render_template('home/index.html', form=form)

@home.route('/help')
def help():
    return render_template('home/help.html')

@home.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('home/user.html', user=user)

@home.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data

        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('home.user', username=current_user.username))
    form.name.data = current_user.name

    return render_template('home/profile.html', form=form)

@home.route('/db')
def query():
    sex = request.args.get('sex')
    class_type = request.args.get('class_type')

    if not sex or not class_type:
        return redirect(url_for('home.index'))

    header = 'id,bbs_id,city,state,latitude,longitude\n'
    if current_user.is_authenticated:
        pass
    else:
        return header + do_query(sex, class_type)

@home.route('/db2')
def name_query():
    name = request.args.get('name')

    if not name:
        return redirect(url_for('home.index'))
    header = 'id,bbs_id,city,state,latitude,longitude\n'
    if current_user.is_authenticated:
        pass
    else:
        return header + do_name_query(name)

    
