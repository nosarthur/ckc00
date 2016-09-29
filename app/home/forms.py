from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Length, Optional, URL, InputRequired, \
                                EqualTo

from ..models import User

class ProfileForm(Form):
    username = StringField('username',
                           validators=[InputRequired(), Length(1, 64)])
    site = StringField('website',
                       validators=[URL(), Optional(), Length(5, 64)])
    city = StringField('city', validators=[Optional(), Length(2, 32)])
    state = StringField('state', validators=[Optional(), Length(2, 32)])
    submit = SubmitField('Submit')

    def __init__(self, old_username, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.old_username = old_username
    def validate(self):
        if not Form.validate(self):
            return False
        if self.username.data == self.old_username:
            return True
        user = User.query.filter_by(username=self.username.data).first()
        if user != None:
            self.username.errors.append('This nickname is already in use. Please choose another one.')
            return False
        return True

class StatForm(Form):
    user_count = StringField('user_count')

class ResetForm(Form):

    old_pwd = PasswordField('old password', validators=[InputRequired()])
    new_pwd = PasswordField('new password',
            validators=[InputRequired(), Length(6, 32), 
            EqualTo('confirm', message='passwords needs to match')])
    confirm = PasswordField('repeat')

    reset = SubmitField('Reset')


class PostForm(Form):
    post = StringField('post', validators=[InputRequired(),
                            Length(1, 140)])
    submit = SubmitField('Submit')
