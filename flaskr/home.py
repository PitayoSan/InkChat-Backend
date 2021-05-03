import functools

from flask import Blueprint, request


bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('', methods=['GET'])
def home():
	return 'This is the InkChat server.'
