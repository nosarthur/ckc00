from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Length, Optional, URL


class ProfileForm(Form):
    username = StringField('username',
                           validators=[Optional(), Length(1, 64)])
    site = StringField('website',
                       validators=[URL(), Optional(), Length(5, 64)])
    submit = SubmitField('Submit')


class StatForm(Form):
    user_count = StringField('user_count')

