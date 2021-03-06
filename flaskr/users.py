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


@bp.route('uid', methods=['GET'])
def get_user_uid():
	if 'username' in request.args:
		username = request.args['username']
		return db.get_user_uid(username)
	return response(400, "username: username of requested user")


@bp.route('', methods=['POST'])
def create_user():
	json_data = request.get_json()
	if 'username' in json_data and 'email' in json_data and 'pw' in json_data:
		username = json_data['username']
		email = json_data['email']
		pw = json_data['pw']
		pp_path = json_data.get('pp', None)
		return db.create_user(username, email, pw, pp_path)
	return response(
		400,
		"username: username of user being created"
		"email: email of user being created"
		"pw: password of user being created"
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
	json_data = request.get_json()
	if 'uid' in json_data and 'encoded_pp' in json_data:
		uid = json_data['uid']
		encoded_pp = json_data['encoded_pp']
		return db.update_user_pp(uid, encoded_pp)
	return response(
		400,
		"uid: uid of owner of the pic"
		"path: path to the file"
	)
