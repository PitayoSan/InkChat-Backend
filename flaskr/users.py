import functools

from flask import Blueprint, request
from flaskr import db


bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('', methods=['GET'])
def get_user():
	if 'username' in request.args:
		username = request.args['username']
	else:
		return 'ERROR: wrong params.\nusername: username of requested user'

	return db.get_user(username)


@bp.route('', methods=['POST'])
def create_user():
	if 'username' in request.args and 'email' in request.args:
		username = request.args['username']
		email = request.args['email']
		pp_path = request.args.get('pp', None)
	else:
		return 'ERROR: wrong params.\nusername: username of user being created\nemail: email of user being created'
	
	return db.create_user(username, email, pp_path)


@bp.route('pp', methods=['GET'])
def get_user_pp():
	if 'username' in request.args:
		username = request.args['username']
	else:
		return 'ERROR: wrong params.\nusername: username of owner of the pic'

	return db.get_user_pp(username)


@bp.route('pp', methods=['POST'])
def update_user_pp():
	if 'username' in request.args and 'path' in request.args:
		username = request.args['username']
		path = request.args['path']
	else:
		return 'ERROR: wrong params.\nusername: username of owner of the pic\npath: path to the file'

	return db.update_user_pp(username, path)
