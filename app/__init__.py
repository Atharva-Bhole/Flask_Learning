from flask import Flask
from app.models import db
from dotenv import load_dotenv
from app.routes import main
import os
load_dotenv()


def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('TRACK_MODIFICATIONS')
    db.init_app(app)
    app.register_blueprint(main)
    return app