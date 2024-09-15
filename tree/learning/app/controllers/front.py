from flask import render_template, redirect, url_for, session, Blueprint
from app.models import set_data_to_db, get_data_from_db, auth
from tree.learning.app.forms import LoginForm, RegisterForm

front = Blueprint('front', __name__)

@front.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data 
        user = auth.create_user_with_email_and_password(email, password)
        auth.send_email_verification(user['IdToken'])
        data = {'name' : name, 'email' : email, 'password' : password, 'isVerified' : False}
        set_data_to_db(data)
        return redirect(url_for('front.login'))

    return render_template('register.html')


@front.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data 
        user = auth.sign_in_with_email_and_password(email, password)
        info = auth.get_account_info(user['idToken'])
        email_verified = info['user'][0]['emailVerified']
        if email_verified:
            session['user_id'] = user['localId']
            user = get_data_from_db(email)
            session['name'] = user['name']
            return redirect(url_for('front.success'))
        else:
            return "<h1>Please Verify your email</h1>",401
    return render_template('login.html')

@front.route('/success')
def success():
    return render_template('firstpage.html')

