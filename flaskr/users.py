import functools
import json

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
	json_data = json.loads(request.get_json())
	if 'uid' in json_data and 'username' in json_data:
		uid = json_data['uid']
		username = json_data['username']
		pp_path = json_data.get('pp', None)
		return db.create_user(uid, username, pp_path)
	return response(
		400,
		"uid: uid of user being created"
		"username: username of user being created"
		"(optional) path: path of the file to upload"
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
	json_data = json.loads(request.get_json())
	if 'uid' in json_data and 'path' in json_data:
		uid = json_data['uid']
		path = json_data['path']
		return db.update_user_pp(uid, path)
	return response(
		400,
		"uid: uid of owner of the pic"
		"path: path to the file"
	)
