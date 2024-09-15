from flask import Flask, render_template, request, redirect, url_for, session, flash
import pyrebase
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

# Replace with your Firebase configuration
config = {
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "apiKey": os.getenv("API_KEY"),
    "authDomain": os.getenv('AUTH_DOMAIN'),
    "projectId": os.getenv('PROJECT_ID'),
    "storageBucket": os.getenv('STORAGE_BUCKET'),
    "messagingSenderId": os.getenv("MESSAGING_SENDER_ID"),
    "appId": os.getenv("APP_ID"),
    "measurementId": os.getenv("MEASUREMENT_ID")
}

# Initialize Firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

# ... other Flask routes and functions

@app.route('/register', methods=['GET', 'POST'])
def register():
    # ... form validation and user creation logic
    user = {'email':'person@gmail.com', 'password':'abcdefgh', 'username' : 'atharva_bhole'}
    # Create a unique key for the user's data
    user_key = db.child("persons").push(user).key
    # ... other success handling, like creating a session or redirecting
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # ... login form processing
    email = 'person@gmail.com'
    password= 'abcdefgh'

    # Authenticate with Firebase
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        session['user_id'] = user['localId']
        # ... other login success handling
        return redirect(url_for('home'))
    except pyrebase.exceptions.FirebaseError:
        # Handle authentication errors
        flash('Invalid email or password')
        return render_template('login.html')

@app.route('/home')
def home():
    # Access user data from Firebase using session['user_id']
    user_data = db.child("persons").child(session['user_id']).get().val()
    return render_template('home.html', user_data=user_data)

if __name__ == '__main__':
    app.run()