from flask import Flask
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

cred = credentials.Certificate("./key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# create/update
doc_ref = db.collection('users').document('alovelace')
doc_ref.set({
    'first': 'Ada',
    'last': 'Lovelace',
    'born': 1815
})

# read
users_ref = db.collection('users')
docs = users_ref.stream()
for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')

@app.route('/')
def hello_world():
	return 'Hello from InkChat!'
