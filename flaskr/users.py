import functools
import json

from flaskr import db
from flask import Blueprint, request
from flaskr.utils.responses import response


bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('', methods=['GET'])
def get_user():
	if 'username' in request.args:
		username = request.args['username']
		return db.get_user(username)
	return response(400, "username: username of requested user")


@bp.route('', methods=['POST'])
def create_user():
	json_data = json.loads(request.get_json())
	if 'username' in json_data and 'email' in json_data:
		username = json_data['username']
		email = json_data['email']
		pp_path = json_data.get('pp', None)
		return db.create_user(username, email, pp_path)
	return response(
		400,
		"username: username of user being created"
		"email: email of user being created"
		"(optional) path: path of the file to upload"
	)


@bp.route('pp', methods=['GET'])
def get_user_pp():
	if 'username' in request.args:
		username = request.args['username']
		return db.get_user_pp(username)
	return response(
		400,
		"username: username of owner of the pic"
	)


@bp.route('pp', methods=['POST'])
def update_user_pp():
	json_data = json.loads(request.get_json())
	if 'username' in json_data and 'path' in json_data:
		username = json_data['username']
		path = json_data['path']
		return db.update_user_pp(username, path)
	return response(
		400,
		"username: username of owner of the pic"
		"path: path to the file"
	)
