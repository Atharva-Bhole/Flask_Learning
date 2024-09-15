from flask import render_template, redirect, url_for, session, Blueprint
from app.models import set_data_to_db, get_data_from_db

front = Blueprint('front', __name__)

@front.route('/register')
def register():
    
    return render_template('register.html')

