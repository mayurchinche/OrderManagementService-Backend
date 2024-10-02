from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity,verify_jwt_in_request, jwt_required as flask_jwt_required

from .jwt_handler import decode_jwt  # Import the decode function
from ..logging.logging_handler import log_request, log_response



def custom_jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):

        token = request.headers.get('Authorization')
        print("token",token)
        if not token:
            return jsonify({"error": "Token is missing!"}), 403

        payload = decode_jwt(token)
        print("payload",payload)
        if not payload:
            return jsonify({"error": "Invalid or expired token!"}), 401

        return fn(*args, **kwargs)

    return wrapper


def jwt_required_with_contact_validation(fn):
    @wraps(fn)
    @flask_jwt_required()
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"error": str(e)}), 401

        contact_number = None
        if request.method == 'GET':
            # Get contact_number from query params in GET request
            contact_number = request.args.get('contact_number')
        elif request.method in ['POST', 'PUT', 'DELETE']:
            # Get contact_number from JSON body in other methods
            data = request.get_json()
            contact_number = data.get('contact_number')

        if not contact_number:
            return jsonify({"error": "Contact number is required."}), 400

        # Get the user identity from JWT
        user_identity = get_jwt_identity()

        # Validate the contact_number matches the JWT identity
        if contact_number != user_identity:
            return jsonify({"error": "Invalid contact number."}), 403

        return fn(*args, **kwargs)

    return wrapper