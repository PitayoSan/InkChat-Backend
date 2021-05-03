import os
import firebase_admin

from firebase_admin import credentials, firestore, storage


def init_db():
    cred = credentials.Certificate('./key.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    return db


def upload_user_pp(username, path):
    try:
        bucket = storage.bucket(os.environ['FS_BUCKET'])
    except KeyError:
        print("Bucket not found in system")
        return "Bucket not found in system"
    
    _, file_extension = os.path.splitext(path)
    pp_name = f"{username}{file_extension}"
    blob = bucket.blob(f"users/pp/{pp_name}")

    file_dir = os.path.dirname(path)
    os.chdir(file_dir)

    file_name = os.path.basename(path)
    with open(file_name, 'rb') as file:
        blob.upload_from_file(file)

    return pp_name

db = init_db()
