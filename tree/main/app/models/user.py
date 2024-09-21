from . import db
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app as app
from sqlalchemy import Sequence, func
import re


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String, primary_key=True)
    gender = db.Column(db.String(length=1))
    address = db.Column(db.String(length=255))
    mobile = db.Column(db.String(length=15))
    name = db.Column(db.String(length=255), nullable=False, unique=True)
    email = db.Column(db.String(length=255), nullable=False, unique=True)
    password = db.Column(db.String(length=255), nullable=False)
    mob_verified = db.Column(db.Boolean(), default=False)
    email_verified = db.Column(db.Boolean(), default=False)

    def get_verification_token(self, expires_sec=3600):
        secret_key = app.config['SECRET_KEY']
        s = Serializer(secret_key=secret_key )
        payload = {'user_id': self.id}
        print(f"Payload: {payload}")
        return s.dumps(payload)

    @staticmethod
    def verify_token(token):
        secret_key = app.config['SECRET_KEY']
        if not secret_key:
            print("No secret key")
            return None
        s = Serializer(secret_key)
        try:
            user_id = s.loads(token)['user_id']
        except Exception as e:
            print(f"Token verification failed: {e}")
            return None
        return Users.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
    @staticmethod
    def generate_custom_id():
        # Get the next value from the PostgreSQL sequence
        next_val = db.session.execute(Sequence('anfa_id_seq'))
        
        # Format it with the prefix and leading zeros
        custom_id = f"ANFA{next_val:03d}"
        return custom_id

    # Override the 'before_insert' event to set the ID
