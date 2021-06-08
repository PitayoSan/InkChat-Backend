import functools
import json

from flaskr import db
from flask import Blueprint, request
from flaskr.utils.responses import response


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('grant', methods=['GET'])
def grant_token():
	if 'Authorization' in request.headers and request.headers['Authorization'].split(' ')[0] == 'Bearer':
		raw_token = request.headers['Authorization']
		token = raw_token.split(' ')[1]
		decoded_token = db.auth.verify_id_token(token)
		if decoded_token:
			return 'true'
		return 'false'
	return response(400, 'No valid Authorization token was found')
