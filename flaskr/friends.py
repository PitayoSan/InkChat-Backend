import functools

from flask import Blueprint, request
from .db import db

bp = Blueprint('friends', __name__, url_prefix='/friends')

@bp.route('', methods=['GET'])
def get_all_friends():
	if 'user' in request.args:
		user = request.args['user']
	else:
		return 'ERROR: wrong params.\nuser: user to get all friends from'
	
	user_doc = db.collection('users').document(user)
	return user_doc.get().to_dict()['friends']


@bp.route('', methods=['POST'])
def send_friend_request():
	if 'sender' in request.args and 'dest' in request.args:
		sender = request.args['sender']
		dest = request.args['dest']
	else:
		return 'ERROR: wrong params.\nsender: user sending friend request\ndest: user the firend request is being sent to'
	
	if sender == dest:
		return 'ERROR: sender and dest can\'t be the same'

	user_doc = db.collection('users').document(dest)
	friends = user_doc.get().to_dict()['friends']
	if sender in friends:
		return 'ERROR: sender is already friends with dest or there is already a pending friend request between them.'
	friends[sender] = False
	user_doc.set({'friends': friends}, merge=True)
	return dest


@bp.route('', methods=['PUT'])
def accept_friend_request():
	if 'sender' in request.args and 'dest' in request.args:
		sender = request.args['sender']
		dest = request.args['dest']
	else:
		return 'ERROR: wrong params.\nsender: user that sent the friend request\ndest: user that is accepting the firend request'
	
	if sender == dest:
		return 'ERROR: sender and dest can\'t be the same'

	dest_doc = db.collection('users').document(dest)
	dest_friends = dest_doc.get().to_dict()['friends']
	if sender not in dest_friends:
		return 'ERROR: there is no pending friend request between sender and dest.'
	dest_friends[sender] = True
	dest_doc.set({'friends': dest_friends}, merge=True)

	sender_doc = db.collection('users').document(sender)
	sender_friends = sender_doc.get().to_dict()['friends']
	sender_friends[dest] = True
	sender_doc.set({'friends': sender_friends}, merge=True)

	return sender


@bp.route('', methods=['DELETE'])
def delete_friend_or_friend_request():
	if 'user' in request.args and 'friend' in request.args:
		user = request.args['user']
		friend = request.args['friend']
	else:
		return 'ERROR: wrong params.\nuser: user that\'s deleting a friend\nfriend: user that\'s being deleted'
	
	if user == friend:
		return 'ERROR: user and friend can\'t be the same'

	user_doc = db.collection('users').document(user)
	user_friends = user_doc.get().to_dict()['friends']
	if friend not in user_friends:
		return 'ERROR: friend isn\'t a friend of user or there is no pending friend request between them.'
	user_friends.pop(friend)
	temp = user_doc.get().to_dict()
	temp['friends'] = user_friends
	user_doc.set(temp)
	
	friend_doc = db.collection('users').document(friend)
	friend_friends = friend_doc.get().to_dict()['friends']
	if user in friend_friends:
		friend_friends.pop(user)
		temp = friend_doc.get().to_dict()
		temp['friends'] = friend_friends
		friend_doc.set(temp)

	return friend
