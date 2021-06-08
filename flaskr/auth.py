import functools
import json

from flaskr import db, pubnub
from flask import Blueprint, request
from flaskr.utils.responses import response


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('grant', methods=['GET'])
def grant_token():
	if 'Authorization' in request.headers and request.headers['Authorization'].split(' ')[0] == 'Bearer':
		raw_token = request.headers['Authorization']
		token = raw_token.split(' ')[1]
		decoded_token = db.auth.verify_id_token(token)
		if not decoded_token:
			return response(403, 'Unauthorized')
		channels = [friend.channel for friend in db.get_all_friends()]
		channels.append(db.get_all_groups())
		pubnub.grant()\
			.auth_keys(token)\
			.channels(channels)\
			.read(True)\
			.write(True)
		return 'true'
	return response(400, 'No valid Authorization token was found')
