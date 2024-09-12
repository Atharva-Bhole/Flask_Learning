from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[])
    email = StringField('email', validators=[])
    password = PasswordField('password', validators=[])
    submit = SubmitField('Register')

class VerifyForm(FlaskForm):
    otp = StringField('otp', validators=[DataRequired()])
    submit = SubmitField('Verify your email')