import functools

from flask import Blueprint, request


bp = Blueprint('test', __name__, url_prefix='/test')

@bp.route('/', methods=['GET'])
def test():
	return "test"
