from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, IntegerField, RadioField, TextAreaField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    gender = RadioField('gender',choices=['Male', 'Female', 'Other'], validators=[DataRequired()])
    address = TextAreaField('address', validators=[DataRequired()])
    mobile = IntegerField('mobile', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Register')

class VerifyForm(FlaskForm):
    otp = StringField('otp', validators=[DataRequired()])
    submit = SubmitField('Verify your email')