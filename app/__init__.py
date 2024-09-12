from flask import Flask
from app.models import db
from dotenv import load_dotenv
from flask_mail import Mail
from flask_bcrypt import Bcrypt
import os

load_dotenv()

bcrypt = Bcrypt()
mail = Mail()
def create_app():
    app = Flask(__name__)
    
    # Load configuration
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

    # Initialize extensions
    mail.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    app.extensions['bcrypt'] = bcrypt
    app.mail = mail

    return app
