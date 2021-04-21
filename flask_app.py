from flask import Flask
from flask import request
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

cred = credentials.Certificate("./key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/', methods=['GET'])
def home():
	return 'This is the InkChat server.'

@app.route('/users', methods=['POST'])
def create_user():
	if 'username' in request.args and 'email' in request.args:
		username = request.args['username']
		email = request.args['email']
	else:
		abort(400)
	
	user_doc = db.collection('users').document(username)
	user_doc.set({
		'username': username,
		'email': email
	})
	return True

@app.route('/friends', methods=['GET'])
def get_all_friends():
	if 'user' in request.args:
		user = request.args['user']
	else:
		abort(400)
	
	user_doc = db.collection('users').document(user)
	return user_doc.get().to_dict()['friends']

@app.route('/friends', methods=['POST'])
def send_friend_request():
	if 'sender' in request.args and 'dest' in request.args:
		sender = request.args['sender']
		dest = request.args['dest']
	else:
		abort(400)
	
	user_doc = db.collection('users').document(sender)
	friends = user_doc.get().to_dict()['friends']
	if dest in friends:
		return False
	friends[dest] = False
	user_doc.set(friends, merge=True)
	return True

@app.route('/friends', methods=['PUT'])
def accept_friend_request():
	if 'sender' in request.args and 'dest' in request.args:
		sender = request.args['sender']
		dest = request.args['dest']
	else:
		abort(400)
	
	user_doc = db.collection('users').document(sender)
	friends = user_doc.get().to_dict()['friends']
	if dest not in friends:
		return False
	friends[dest] = True
	user_doc.set(friends, merge=True)
	return True

@app.route('/friends', methods=['DELETE'])
def delete_friend_or_friend_request():
	if 'user' in request.args and 'friend' in request.args:
		user = request.args['user']
		friend = request.args['friend']
	else:
		abort(400)
	
	user_doc = db.collection('users').document(user)
	friends = user_doc.get().to_dict()['friends']
	if friend not in friends:
		return False
	friends.pop(friend)
	user_doc.set(friends, merge=True)
	return True
