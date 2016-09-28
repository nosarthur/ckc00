from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Length, Optional, URL, InputRequired, \
                                EqualTo


class ProfileForm(Form):
    username = StringField('username',
                           validators=[Optional(), Length(1, 64)])
    site = StringField('website',
                       validators=[URL(), Optional(), Length(5, 64)])
    submit = SubmitField('Submit')


class StatForm(Form):
    user_count = StringField('user_count')

class ResetForm(Form):

    old_pwd = PasswordField('old password', validators=[InputRequired()])
    new_pwd = PasswordField('new password',
            validators=[InputRequired(), Length(6, 25), 
            EqualTo('confirm', message='passwords needs to match')])
    confirm = PasswordField('repeat')

    reset = SubmitField('Reset')
