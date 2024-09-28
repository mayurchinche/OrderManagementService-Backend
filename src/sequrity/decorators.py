from functools import wraps
from flask import request, jsonify
from .jwt_handler import decode_jwt  # Import the decode function

def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token is missing!"}), 403

        payload = decode_jwt(token)
        if not payload:
            return jsonify({"error": "Invalid or expired token!"}), 403

        return fn(*args, **kwargs)

    return wrapper
