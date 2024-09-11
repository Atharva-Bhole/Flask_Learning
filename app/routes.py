from flask import Flask, render_template, redirect, Blueprint, url_for, flash, request
from app.models import db, Users
from app import  bcrypt
from flask import current_app as app
from .gmail_service import send_email
from googleapiclient.errors import HttpError

from flask_mail import Message
from app.forms import LoginForm, RegisterForm
main = Blueprint('main', __name__)


@main.route('/')
def land():
    return render_template('home.html')

@main.route('/about/<username>')
def about(username):
    users = [
        {'id':1, 'name' : 'Roal', 'email':'Royal@abcd.in' },
        {'id':2, 'name' : 'Royl', 'email':'Royal@acd.in' },
        {'id':3, 'name' : 'Royal', 'email':'Royal@abd.in' }
    ]
    return render_template('about.html', name = username, users=users)

@main.route('/firstpage')
def firstpage():
    return render_template('firstpage.html', user = request.args.user)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.is_verified:
                return redirect(url_for('firstpage'), user=user)
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def page1():
    form = RegisterForm()
    if form.validate_on_submit():
        passwd = form.password.data
        hashedpwd = bcrypt.generate_password_hash(passwd).decode('utf-8')
        user_to_create = Users(username=form.username.data,email = form.email.data,password = hashedpwd)
        db.session.add(user_to_create)
        db.session.commit()
        print("Hello")
        send_verification_email(user_to_create)
        print('Hi')
        print("Verification mail Sent")
        return redirect(url_for('main.login'))
    else:
        print("form not validated")
    return render_template('register.html', form=form)


@main.route('/verify/<token>')
def verify(token):
    user = Users.verify_token(token)
    if user is None:
        flash("Invalid Token or expired token")
        return redirect(url_for('main.register'))
    user.is_verified = True
    db.session.commit()
    flash("Verified successfully")
    print("Success")
    return redirect(url_for('main.login'))

from sqlalchemy.orm.exc import ObjectDeletedError

def send_verification_email(user):
    try:
        # Retrieve the user from the database
        user = Users.query.get(user.id)
        if user is None:
            raise ValueError("User does not exist.")
        
        # Generate the verification token
        token = user.get_verification_token()
        print("Token Worked")
        
        # Construct the email subject and body
        subject = 'Email Verification'
        body = f'''To verify your account, visit the following link:
{url_for('main.verify', token=token, _external=True)}
If you did not make this request, simply ignore this email.
'''

        # Send the email using Google API
        send_email(subject, body, user.email)
        print("Message Sent")

    except ValueError as e:
        print(f"Error: {e}")
    except HttpError as e:
        print(f"An error occurred: {e}")