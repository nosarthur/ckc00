import io
import csv
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask.ext.login import login_required, current_user

from . import home
from .forms import ProfileForm, StatForm, ResetForm, PostForm
from .. import db
from ..models import User, Post


@home.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home/index.html')


@home.route('/help')
def help():
    form = StatForm()
    form.user_count = User.query.filter(User.email.isnot(None)).count()
    return render_template('home/help.html', form=form)


@home.route('/user/<username>', methods=['GET', 'POST'])
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = PostForm()
    
    if current_user.is_authenticated and form.submit.data \
            and form.validate_on_submit():
        post = Post(body=form.post.data,
                    timestamp=datetime.utcnow(),
                    author=current_user)
        current_user.awards += 1
        db.session.add(post)
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your post is now live!')

    posts = user.posts.all()
    if current_user.is_authenticated:
        posts.extend(user.liked.all())

    return render_template('home/user.html', user=user, 
                            form=form, posts=posts)


@home.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form_profile = ProfileForm(current_user.username)
    form_reset = ResetForm()

    if form_profile.submit.data and form_profile.validate_on_submit():
        if not current_user.site and form_profile.site.data:
            current_user.awards += 1
        elif current_user.site and not form_profile.site.data:
            current_user.awards -= 1

        current_user.username = form_profile.username.data
        current_user.site = form_profile.site.data

        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('home.user',
                        username=current_user.username))
    form_profile.username.data = current_user.username
    form_profile.site.data = current_user.site

    if form_reset.reset.data and form_reset.validate_on_submit():
        if not current_user.verify_password(form_reset.old_pwd.data):
            flash('Invalid password.')
            return redirect(url_for('home.profile'))

        current_user.password = form_reset.confirm.data
        db.session.add(current_user._get_current_object())
        db.session.commit()

        flash('Your password has been updated.')
        return redirect(url_for('home.user', 
                                username=current_user.username))

    return render_template('home/profile.html', 
                form_profile=form_profile, 
                form_reset=form_reset)


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

    filters = {}
    if sex != 'all':
        filters['sex'] = sex
    if class_type != 'all':
        filters['class_type'] = class_type
    rows = q.filter_by(**filters)

    writer.writerows(rows)
    return output.getvalue()


@home.before_request
def before_request():
    user = current_user
    if user.is_authenticated:
        user.last_seen = datetime.utcnow()
        db.session.add(user)
        db.session.commit()


@home.app_errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403

@home.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@home.app_errorhandler(500)
def not_found_error(error):
    return render_template('500.html'), 500


