import functools

from flask import Blueprint, request
from .db import db


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
