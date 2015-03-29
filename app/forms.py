from flask.ext.wtf import Form
from wtforms import StringField, BooleanField,TextField,PasswordField,IntegerField
from wtforms.validators import DataRequired


class LoginForm(Form):
    openid = TextField('openid', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    passwordre = PasswordField('passwordre', validators=[DataRequired()])

class SigninForm(Form):
    idu = StringField('idu', validators=[DataRequired()])
    passcode = PasswordField('passcode', validators=[DataRequired()])

class EnteryForm(Form):
    student = StringField('student', validators=[DataRequired()])
    mark = IntegerField('mark', validators=[DataRequired()])

class DataForm(Form):
    says = TextField('says', validators=[DataRequired()])

