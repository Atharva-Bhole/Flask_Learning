from firebase_admin import credentials, auth, db
import firebase_admin
from dotenv import load_dotenv
import os
load_dotenv()
def initialize_fb():
    cred = credentials.Certificate("C:/Users/Mehul Mahajan/Github/Flask_Learning/tree/learning/app/models/credentials.json")
    firebase_admin.initialize_app(cred, {'databaseURL' : os.getenv("FIREBASE_DATA_URL")})

def get_data_from_db(email):
    ref = db.reference(f'/users/{email}')
    return ref.get()

def set_data_to_db(data):
    collection = data['email']
    ref = db.reference(f'/users/{collection}')
    ref.set(data)

initialize_fb()