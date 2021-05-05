import functools
import json

from flaskr import db
from flask import Blueprint, request
from flaskr.utils.responses import response


bp = Blueprint('friends', __name__, url_prefix='/friends')

@bp.route('', methods=['GET'])
def get_all_friends():
	if 'username' in request.args:
		username = request.args['username']
		return db.get_all_friends(username)
	return response(400, "username: user to get all friends from")


@bp.route('', methods=['POST'])
def send_friend_request():
	json_data = json.loads(request.get_json())
	if 'sender' in json_data and 'dest' in json_data:
		sender = json_data['sender']
		dest = json_data['dest']
		if sender == dest:
			return response(400, "sender and dest can't be the same")
		return db.send_friend_request(sender, dest)
	return response(
		400,
		"sender: user sending friend request"
		"dest: user the friend request is being sent to"
	)


@bp.route('', methods=['PUT'])
def accept_friend_request():
	json_data = json.loads(request.get_json())
	if 'sender' in json_data and 'dest' in json_data:
		sender = json_data['sender']
		dest = json_data['dest']
		if sender == dest:
			return response(400, "sender and dest can't be the same")
		return db.accept_friend_request(sender, dest)
	return response(
		400,
		"sender: user that sent the friend request"
		"dest: user that is accepting the friend request"
	)


@bp.route('', methods=['DELETE'])
def delete_friend_or_friend_request():
	if 'username' in request.args and 'friend' in request.args:
		username = request.args['username']
		friend = request.args['friend']
		if username == friend:
			return response(400, "username and friend can't be the same")
		return db.delete_friend_or_friend_request(username, friend)
	return response(
		400,
		"username: user that's deleting a friend"
		"friend: user that's being deleted"
	)
