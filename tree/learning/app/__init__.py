from flask import Flask
from dotenv import load_dotenv
import os

from tree.learning.app.controllers import admin
load_dotenv()

def create_app():
    app = Flask(__name__)

    from tree.learning.app.controllers import front
    app.register_blueprint(front)
    app.register_blueprint(admin)
    
    return app