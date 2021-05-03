import functools

from flask import Blueprint, request
from flaskr import db

bp = Blueprint('friends', __name__, url_prefix='/friends')

@bp.route('', methods=['GET'])
def get_all_friends():
	if 'username' in request.args:
		username = request.args['username']
	else:
		return 'ERROR: wrong params.\nusername: user to get all friends from'
	
	return db.get_all_friends(username)


@bp.route('', methods=['POST'])
def send_friend_request():
	if 'sender' in request.args and 'dest' in request.args:
		sender = request.args['sender']
		dest = request.args['dest']
	else:
		return 'ERROR: wrong params.\nsender: user sending friend request\ndest: user the firend request is being sent to'
	
	if sender == dest:
		return 'ERROR: sender and dest can\'t be the same'

	return db.send_friend_request(sender, dest)


@bp.route('', methods=['PUT'])
def accept_friend_request():
	if 'sender' in request.args and 'dest' in request.args:
		sender = request.args['sender']
		dest = request.args['dest']
	else:
		return 'ERROR: wrong params.\nsender: user that sent the friend request\ndest: user that is accepting the firend request'
	
	if sender == dest:
		return 'ERROR: sender and dest can\'t be the same'

	return db.accept_friend_request(sender, dest)


@bp.route('', methods=['DELETE'])
def delete_friend_or_friend_request():
	if 'username' in request.args and 'friend' in request.args:
		username = request.args['username']
		friend = request.args['friend']
	else:
		return 'ERROR: wrong params.\nusername: user that\'s deleting a friend\nfriend: user that\'s being deleted'
	
	if user == friend:
		return 'ERROR: user and friend can\'t be the same'

	return db.delete_friend_or_friend_request(username, friend)
