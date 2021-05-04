import functools

from flask import Blueprint, request
from flaskr.utils.responses import response


bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('', methods=['GET'])
def home():
	return response(200, "This is the InkChat server")
