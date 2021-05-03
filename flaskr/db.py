import firebase_admin

from firebase_admin import credentials, firestore


def init_db():
    cred = credentials.Certificate('./key.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    return db


db = init_db()
