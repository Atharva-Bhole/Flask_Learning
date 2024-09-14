from flask import render_template, redirect, url_for, session, Blueprint
from flask import current_app
from app.forms import LoginForm, RegisterForm
from firebase import auth, db

main = Blueprint('main', __name__)
@main.route('/')
def land():
    return render_template("base.html")

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        try:
            user = {'username':username, 'email':email, 'password':password}
            person = auth.create_user_with_email_and_password(email, password)
            auth.sign_in_with_email_and_password(email,password)
            session['person'] = username
            db.child('users').child(person['localId']).set(user)
            return redirect(url_for('main.login'))
        except:
            return "<h1>Problems with registration</h1>"
    return render_template('register.html', form=form)
    