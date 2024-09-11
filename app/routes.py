from flask import Flask, render_template, redirect, Blueprint, session, url_for, flash, request
from app.models import db, Users
from app import  bcrypt
from flask import current_app as app
from flask_mail import Message
from flask import current_app as app

from app.forms import LoginForm, RegisterForm, VerifyForm
from app.oauth import load_oauth_credentials, send_gmail_api_message
main = Blueprint('main', __name__)


@main.route('/')
def land():
    msg = Message('Test Email', sender='atharvabhole239@gmail.com', recipients=['atharvabholeofficial@gmail.com'])
    msg.body = 'This is a Test Mail'
    app.mail.send(msg)

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

        token = user_to_create.get_verification_token()
        subject = 'Email Verification'
        body = f'To verify your account, visit the following link: {url_for("main.verify", token=token, _external=True)}'
        send_gmail_api_message(user_to_create.email, subject, body)

        return redirect(url_for('main.login'))
    else:
        print("form not validated")
    return render_template('register.html', form=form)

@main.route('/oauth2callback')
def oauth2callback():
    flow = load_oauth_credentials()
    flow.fetch_token(authorization_response=request.url)
    creds = flow.credentials
    session['token'] = creds.token
    flash("OAuth authentication successful!", 'success')
    return redirect(url_for('home'))

@main.route('/verify/<token>')
def verify(token):
    form = VerifyForm()
    if form.validate_on_submit():

        user = Users.verify_token(token)
        if user is None:
            flash("Invalid Token or expired token")
            return redirect(url_for('main.register'))
        user.is_verified = True
        db.session.commit()
        flash("Verified successfully")
        print("Success")
        return redirect(url_for('main.verifypage'))


def send_verification_email(user, token):
    msg = Message('Email Verification', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To verify your account, click on the following link:
                {url_for('verify_email', token=token, _external=True)}
                If you did not request this, please ignore this email.
                '''
    mail.send(msg)
