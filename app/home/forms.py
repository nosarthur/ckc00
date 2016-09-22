from flask.ext.wtf import Form
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import Length, Optional, URL 

class ProfileForm(Form):
    username = StringField('username', 
                            validators=[Optional(), Length(1, 64)])
    site = StringField('website', 
                   validators=[URL(), Optional(), Length(5, 64)])
    submit = SubmitField('Submit')

class QueryForm(Form):
    sex_select = SelectField('Sex', choices=[('all', 'All'), ('m', 'Male'), ('f', 'Female')])
    class_select = SelectField('Class', choices=[('all', 'All'), 
                                            ('mixed', 'Mixed'), 
                                            ('litart', 'Lit. Art'), 
                                            ('science', 'Science'),
                                            ('eduexp', 'Edu. Exp.')])
#    name = StringField('Search', validators=[Optional()], 
#                       render_kw={'placeholder':'First Last'})
