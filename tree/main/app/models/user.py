from . import db
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app as app


class Users(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=255), nullable=False, unique=True)
    email = db.Column(db.String(length=255), nullable=False, unique=True)
    password = db.Column(db.String(length=255), nullable=False)
    is_verified = db.Column(db.Boolean(), default=False)

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