import io
import csv
from flask import render_template, flash, redirect, url_for, request
from flask.ext.login import login_required, current_user

from . import home
from .forms import ProfileForm
from .. import db
from ..models import User

@home.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home/index.html')

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
        username = form.username.data
        user = User.query.filter_by(username=username).first()        
        if not user or user.id == current_user.id:
            current_user.username = username
        else:
            flash('This username is already taken.')
            return redirect(url_for('home.profile'))
        current_user.site = form.site.data

        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('home.user', username=current_user.username))
    form.username.data = current_user.username
    form.site.data = current_user.site

    return render_template('home/profile.html', form=form)

@home.route('/db')
def query():
    sex = request.args.get('sex')
    class_type = request.args.get('class_type')
    name = request.args.get('name')

    output = io.BytesIO()
    writer = csv.writer(output)

    cols = ['id', 'display_name', 'city', 'state', 'latitude', 'longitude']
    writer.writerow(cols)
    if current_user.is_authenticated:
        cols[1] = 'name'
    else:
        cols[1] = 'bbs_id'
    q = User.query.with_entities(*(getattr(User, col) for col in cols))

    if name: # name query
        rows = q.filter_by(name=name)
        writer.writerows(rows)
        return output.getvalue()

    if not sex or not class_type:
        return redirect(url_for('home.index'))

    if sex=='all' and class_type=='all':
        rows = q.all()
    elif sex=='all' and class_type!='all':
        rows = q.filter_by(class_type=class_type)
    elif sex!='all' and class_type=='all':
        rows = q.filter_by(sex=sex)
    else:
        rows = q.filter_by(sex=sex, class_type=class_type)
    
    writer.writerows(rows)
    return output.getvalue()

   
