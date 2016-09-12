from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired

class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default = False)

class ScrapeForm(Form):
    src = BooleanField('src', default=False)  #False for AO3, True for IG
    uname = StringField('uname', validators=[DataRequired()])
    pseud = StringField('pseud', validators=[DataRequired()])
    picCodes = TextAreaField('picCodes')