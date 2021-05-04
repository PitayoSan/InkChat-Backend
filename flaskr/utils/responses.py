from flask import jsonify


def response(code: int(), data: str()):
    return jsonify(data=data), code
