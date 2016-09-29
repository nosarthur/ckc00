from flask import render_template, current_app, request, \
                  redirect, url_for, flash
from flask.ext.login import login_user, logout_user, login_required

from . import auth
from .forms import LoginForm
from ..models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    print 'debug? ', current_app.config['DEBUG']
    print 'key? ', current_app.config['SECRET_KEY']
    print current_app.config['SQLALCHEMY_DATABASE_URI']
    if not current_app.config['DEBUG'] \
       and not current_app.config['TESTING'] \
       and not request.is_secure:
        return redirect(url_for('.login', _external=True, _scheme='https'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash('Who are you?')
            return redirect(url_for('.login'))
        login_user(user, form.remember_me.data)
        return redirect(request.args.get('next') or url_for('home.index'))
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Come again~~')
    return redirect(url_for('home.index'))
