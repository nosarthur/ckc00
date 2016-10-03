from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import Length, Optional, URL, InputRequired, \
                                EqualTo, Email

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


class ReferForm(Form):
    name = StringField('name', validators=[InputRequired(), 
                                           Length(max=32)])
    email = StringField('Email', validators=[InputRequired(),
                                             Length(10, 64), Email()])
    class_type = SelectField('Class', choices=[('mixed', 'Mixed'),
                           ('litart', 'Lit. Art'),
                           ('science', 'Science'), 
                           ('eduexp', 'Edu. Exp.')])
    note = StringField('Note', validators=[Optional(), 
                                                 Length(max=64)])
    submit = SubmitField('Submit')

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
