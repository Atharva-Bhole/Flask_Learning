from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='view', static_folder='view/static')
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    from app.controllers.front import front
    app.register_blueprint(front)
    
    return app