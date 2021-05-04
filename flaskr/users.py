import functools

from flaskr import db
from flask import Blueprint, request
from flaskr.utils.responses import response


bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('', methods=['GET'])
def get_user():
	if 'uid' in request.args:
		uid = request.args['uid']
		return db.get_user(uid)
	return response(400, "uid: uid of requested user")


@bp.route('', methods=['POST'])
def create_user():
	if 'uid' in request.args and 'username' in request.args and 'email' in request.args:
		uid = request.args['uid']
		username = request.args['username']
		email = request.args['email']
		pp_path = request.args.get('pp', None)
		return db.create_user(uid, username, email, pp_path)
	return response(
		400,
		"uid: uid of user being created"
		"username: username of user being created"
		"email: email of user being created"
	)


@bp.route('pp', methods=['GET'])
def get_user_pp():
	if 'uid' in request.args:
		uid = request.args['uid']
		return db.get_user_pp(uid)
	return response(
		400,
		"uid: uid of owner of the pic"
	)


@bp.route('pp', methods=['POST'])
def update_user_pp():
	if 'uid' in request.args and 'path' in request.args:
		uid = request.args['uid']
		path = request.args['path']
		return db.update_user_pp(uid, path)
	return response(
		400,
		"uid: uid of owner of the pic"
		"path: path to the file"
	)
