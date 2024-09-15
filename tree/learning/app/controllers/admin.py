from flask import render_template, redirect, url_for, session, Blueprint
from app.models import set_data_to_db, get_data_from_db

admin = Blueprint('admin', __name__)

@admin.route('/adminlog')
def adminlog():
    return render_template('adminlogin.html')