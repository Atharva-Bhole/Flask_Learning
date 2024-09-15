from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])