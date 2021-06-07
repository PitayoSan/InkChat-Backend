import functools
import json

from flaskr import db
from flask import Blueprint, request
from flaskr.utils.responses import response

bp = Blueprint('groups', __name__, url_prefix='/groups')

@bp.route('all', methods=['GET'])
def get_all_groups():
	return db.get_all_groups()

@bp.route('', methods=['POST'])
def create_group():
	json_data = request.get_json()
	if 'name' in json_data:
		name = json_data['name']
		return db.create_group(name)
	return response(
		400,
		"name: name of group being created"
	)

@bp.route('', methods=['GET'])
def get_group():
	if 'name' in request.args:
		name = request.args['name']
		return db.get_group(name)
	return response(400, "name: name of requested group")

@bp.route('', methods=['PUT'])
def send_message():
	json_data = request.get_json()
	if 'name' in json_data and 'msg' in json_data and 'uid' in json_data and 'username' in json_data and "time" in json_data:
		name = json_data['name']
		msg = json_data['msg']
		uid = json_data['uid']
		username = json_data['username']
		time = json_data['time']
		pp = json_data.get('pp', None)
		return db.send_message(name, msg, uid, username, time, pp)
	return response(
		400,
		"name: name of group"
		"msg: message content"
		"uid: uid of user sending message"
		"username: username of user being created"
		"(optional) pp: url of profile picture"
	)
