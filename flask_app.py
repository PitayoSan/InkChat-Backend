from flask import Flask
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': 'inkchat-58958',
})
db = firestore.client()

@app.route('/')
def hello_world():
    return 'Hello from InkChat!'
