import pyrebase
from dotenv import load_dotenv
import os

config = {
    "databaseURL": os.getenv("FIREBASE_DATA_URL"),
    "apiKey": os.getenv("API_KEY"),
  "authDomain": os.getenv('AUTH_DOMAIN'),
  "projectId": os.getenv('PROJECT_ID'),
  "storageBucket": os.getenv('STORAGE_BUCKET'),
  "messagingSenderId": os.getenv("MESSAGING_SENDER_ID"),
  "appId": os.getenv("APP_ID"),
  "measurementId": os.getenv("MEASUREMENT_ID")
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


