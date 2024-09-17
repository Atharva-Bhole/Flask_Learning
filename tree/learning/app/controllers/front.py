from flask import render_template, redirect, url_for, session, Blueprint
from app.models import set_data_to_db, get_data_from_db, register_pyreb, login_w_pyreb
from app.forms import LoginForm, RegisterForm

front = Blueprint('front', __name__)

@front.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data 
        register_pyreb(email, password)
        data = {'name' : name, 'email' : email}
        set_data_to_db(data)

        return redirect(url_for('front.login'))

    return render_template('register.html', form=form)


@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data 
        info = login_w_pyreb(email, password)
        if info:
            email_verified = info['users'][0]['emailVerified']
            print(info['users'])
            if email_verified:
                session['user_id'] = info['users'][0]['localId']
                user = get_data_from_db(email)
                session['name'] = user['name']
                return redirect(url_for('front.success'))
            else:
                return "<h1>Please Verify your email</h1>",401
        else:
            return "<h1>Failed to Fetch User</h1>"
    return render_template('login.html', form=form)

@front.route('/success')
def success():
    return render_template('firstpage.html')


