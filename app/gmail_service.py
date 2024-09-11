import base64
from google.auth.transport.requests import Request
import os
import pickle
from google.oauth2 import service_account
from googleapiclient.discovery import build
from flask import current_app

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
SERVICE_ACCOUNT_FILE = './app/flask-435309-64f71c33e03e.json'  # Update this path

def get_gmail_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

def send_email(subject, body, to):
    service = get_gmail_service()
    message = {
        'raw': base64.urlsafe_b64encode(f'To: {to}\nSubject: {subject}\n\n{body}'.encode()).decode()
    }
    send_message = service.users().messages().send(userId='me', body=message).execute()
    return send_message
