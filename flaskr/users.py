import functools

from flask import Blueprint, request
from .db import db, upload_user_pp


bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('', methods=['POST'])
def create_user():
	if 'username' in request.args and 'email' in request.args:
		username = request.args['username']
		email = request.args['email']
	else:
		return 'ERROR: wrong params.\nusername: username of user being created\nemail: email of user being created'
	
	user_doc = db.collection('users').document(username)
	user_doc.set({
		'username': username,
		'email': email,
		'friends': {}
	})
	return username


@bp.route('pp', methods=['POST'])
def update_user_pp():
	if 'username' in request.args and 'path' in request.args:
		username = request.args['username']
		path = request.args['path']
	else:
		return 'ERROR: wrong params.\nusername: username of owner of the pic\npath: path to the file'

	return upload_user_pp(username, path)
