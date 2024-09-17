from firebase_admin import credentials, auth, db
import firebase_admin
import pyrebase
from dotenv import load_dotenv
import os
load_dotenv()
def initialize_fb():
    cred = credentials.Certificate("C:/Users/Mehul Mahajan/Github/Flask_Learning/tree/learning/app/models/credentials.json")
    firebase_admin.initialize_app(cred, {'databaseURL' : os.getenv("DATABASE_URL")})

pyrebase_config = {
    "apiKey": "AIzaSyBJSiA5CGrnOiZGOlp6jjqFRYlkwf078mY",
    "authDomain": "flask-6eca7.firebaseapp.com",
    "databaseURL": "https://flask-6eca7-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "flask-6eca7",
    "storageBucket": "flask-6eca7.appspot.com",
    "messagingSenderId": "366006503606",
    "appId": "1:366006503606:web:7715460af9e58015cafe17",
    "measurementId" : "G-V5V0L6E5LB"
}

firebase = pyrebase.initialize_app(pyrebase_config)
pb_auth = firebase.auth()

def get_data_from_db(email):
    ref = db.reference(f'/users')
    users = ref.get()
    for key, user_data in users.items():
        if user_data.get('email') == email:
            return user_data
    return None

def set_data_to_db(data):
    name = data['name']
    ref = db.reference(f'/users/{name}')
    ref.set(data)

def register_pyreb(email, password):
    user = pb_auth.create_user_with_email_and_password(email, password)
    pb_auth.send_email_verification(user["idToken"])
    return user

def login_w_pyreb(email ,password):
    user = pb_auth.sign_in_with_email_and_password(email, password)    
    user_info = pb_auth.get_account_info(user['idToken'])
    if user_info:
        return user_info
    else:
        return None
    
    

initialize_fb()