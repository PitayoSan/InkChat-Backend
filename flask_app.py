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
		'email': email,
		'friends': {}
	})
	return username

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
	
	user_doc = db.collection('users').document(dest)
	friends = user_doc.get().to_dict()['friends']
	if source in friends:
		return 'ERROR: sender is already friends with dest or there is already a pending friend request.'
	friends[sender] = False
	user_doc.set(friends, merge=True)
	return dest

@app.route('/friends', methods=['PUT'])
def accept_friend_request():
	if 'sender' in request.args and 'dest' in request.args:
		sender = request.args['sender']
		dest = request.args['dest']
	else:
		abort(400)
	
	dest_doc = db.collection('users').document(dest)
	dest_friends = dest_doc.get().to_dict()['friends']
	if sender not in dest_friends:
		return 'ERROR: there is no pending friend request between sender and dest.'
	dest_friends[sender] = True
	dest_doc.set(friends, merge=True)

	sender_doc = db.collection('users').document(sender)
	sender_friends = sender_doc.get().to_dict()['friends']
	sender_friends[dest] = True
	sender_doc.set(friends, merge=True)

	return sender

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
		return 'ERROR: friend isn\'t a friend of user or there is no pending friend request between them.'
	friends.pop(friend)
	user_doc.set(friends, merge=True)
	return friend
