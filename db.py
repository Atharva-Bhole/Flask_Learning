from app.models import db
from . import app

with app.app_context():
    db.create_all()