from flask import Flask, render_template, redirect, url_for, request
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

app = Flask(__name__)

# Configure Google Drive API credentials
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'credentials.json'

# Google Drive API setup
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=creds)

# Function to read content from a Google Doc file
def get_document_content(file_id):
    try:
        doc = drive_service.files().export(fileId=file_id, mimeType='text/plain').execute()
        content = doc.decode('utf-8')
        return content.splitlines()
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

@app.route('/')
def home():
    return render_template('flipcards.html', cards=[])

@app.route('/upload', methods=['POST'])
def upload():
    file_id = request.form['file_id']
    lines = get_document_content(file_id)
    cards = [{"question": line.split('|')[0], "answer": line.split('|')[1]} for line in lines if '|' in line]
    return render_template('flipcards.html', cards=cards)

if __name__ == '__main__':
    app.run(debug=True)

