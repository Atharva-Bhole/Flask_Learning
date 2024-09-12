from flask import Flask, render_template, redirect, Blueprint, session, url_for, flash, request, session
from app.models import db, Users
import math
from flask_mail import Message
from flask import current_app as app
import random
from app.forms import LoginForm, RegisterForm, VerifyForm


main = Blueprint('main', __name__)

@main.route('/')
def land():
    msg = Message('Test Email', sender=app.config.get('MAIL_DEFAULT_SENDER'), recipients=['atharvabholeofficial@gmail.com'])
    msg.body = 'This is a Test Mail'
    try:
        app.mail.send(msg)
        return "Email sent!"
    except Exception as e:
        return str(e)

@main.route('/about/<username>')
def about(username):
    users = [
        {'id':1, 'name' : 'Roal', 'email':'Royal@abcd.in' },
        {'id':2, 'name' : 'Royl', 'email':'Royal@acd.in' },
        {'id':3, 'name' : 'Royal', 'email':'Royal@abd.in' }
    ]
    return render_template('about.html', name=username, users=users)

@main.route('/firstpage')
def firstpage():
    return render_template('firstpage.html', user=request.args.get('user'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = Users.query.filter_by(email=email).first()
        if user and app.extensions['bcrypt'].check_password_hash(user.password, password):
            if user.is_verified:
                return redirect(url_for('main.firstpage'))
            else:
                print("User not verified")
        else:
            print("Wrong password")
    else:
        print("Form not validated")
    return render_template('login.html', form=form)


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        if not username or not email or not password:
            print("All fields must be filled out.", "error")
            return render_template('register.html', form=form)
        
        sender = app.config.get('MAIL_USERNAME')  # Use get() to avoid KeyError
        
        if sender is None:
            print("Mail sender is not configured.", "error")
            return render_template('register.html', form=form)
        
        otp = generateOTP()
         
        msg = Message(subject='Hello from the other side!',
                  recipients=['atharvabholeofficial@gmail.com'])
        msg.body = f"This mail is for verification please enter the otp {otp} on the page"
        try:
            app.mail.send(msg)
            print("Mail sent")
            print(otp)
            session['username'] = username
            session['email'] = email
            session['password'] = password
            session['otp'] = otp
            return redirect(url_for('main.verifyotp'))
        except Exception as e:
            print(f"Failed to send email: {e}", "error")
            return render_template('register.html', form=form)
    else:
        print("Form not validated")
    return render_template('register.html', form=form)


@main.route('/verifyotp1', methods=['GET', 'POST'])
def verifyotp():
    form = VerifyForm()
    if form.validate_on_submit():
        otp = session.get('otp')
        if otp is None:
            return "No OTP provided", 400 
        tocheckotp = form.otp.data
        print(tocheckotp)
        username = session.get('username')
        password = session.get('password')
        email = session.get('email')
        print(otp)
        if tocheckotp == otp:
            hashedpwd = app.extensions['bcrypt'].generate_password_hash(password).decode('utf-8')
            user_to_create = Users(username=username, email=email, password=hashedpwd, is_verified=True)
            db.session.add(user_to_create)
            db.session.commit()
            return redirect(url_for('main.login'))
        else:
            print("False OTP")
    else:
        print("Form not validated")
    return render_template('verifyotp.html', form=form)

def generateOTP():
    digits = '0123456789'
    OTP = ''.join(random.choice(digits) for i in range(4))
    return OTP
