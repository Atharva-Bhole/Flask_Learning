import pyrebase

config = {
    "databaseURL": 'https://console.firebase.google.com/u/0/project/flask-6eca7/database/flask-6eca7-default-rtdb/data/~2F',
    "apiKey": "AIzaSyBJSiA5CGrnOiZGOlp6jjqFRYlkwf078mY",
  "authDomain": "flask-6eca7.firebaseapp.com",
  "projectId": "flask-6eca7",
  "storageBucket": "flask-6eca7.appspot.com",
  "messagingSenderId": "366006503606",
  "appId": "1:366006503606:web:7715460af9e58015cafe17",
  "measurementId": "G-V5V0L6E5LB"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

