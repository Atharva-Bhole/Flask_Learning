from firebase_admin import credentials, auth, db
import firebase_admin
from dotenv import load_dotenv
import os
load_dotenv()
def initialize_fb():
    cred = credentials.Certificate("C:/Users/ASUS/Desktop/Project/tree/learning/app/models/flask-6eca7-firebase-adminsdk-5im5z-5bd5f9d122.json")
    firebase_admin.initialize_app(cred, {'databaseURL' : os.getenv("FIREBASE_DATA_URL")})

def get_data_from_db(name):
    ref = db.reference(f'/users/{name}')
    return ref.get()

def set_data_to_db(data):
    collection = data['name']
    ref = db.reference(f'/users/{collection}')
    ref.set(data)
initialize_fb()