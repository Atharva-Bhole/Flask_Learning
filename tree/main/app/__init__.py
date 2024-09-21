from flask import Flask
from app.models import db
from dotenv import load_dotenv
from flask_mail import Mail
import os
load_dotenv()
from flask_bcrypt import Bcrypt
mail = Mail()
bcrypt = Bcrypt()
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('TRACK_MODIFICATIONS')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS")
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_DEBUG'] = os.getenv('MAIL_DEBUG')
    bcrypt.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    app.extensions['bcrypt'] = bcrypt
    from app.routes import main
    app.register_blueprint(main)
    with app.app_context():
        db.create_all()

    app.mail = mail
    
    return app
