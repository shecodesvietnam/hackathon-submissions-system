import jwt
from functools import wraps
from flask import request, current_app, jsonify


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'X-Access-Token' in request.headers:
            token = request.headers['X-Access-Token']

        if not token:
            return jsonify('Token is missing!'), 401
            
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return f(data, *args, **kwargs)
        except Exception as e:
            return jsonify('Token is invalid!'), 401
            # raise e

    return decorated