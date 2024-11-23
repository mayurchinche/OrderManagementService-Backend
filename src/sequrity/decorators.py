import json
from functools import wraps

from flask import request, jsonify, Response
from flask_jwt_extended import get_jwt_identity,verify_jwt_in_request, jwt_required as flask_jwt_required

from .jwt_handler import decode_jwt  # Import the decode function
from ..exception.global_exception_handler import handle_exception
from ..logging.logging_handler import log_request, log_response


# Wrapper function to apply the decorators automatically
def apply_decorators(allowed_roles=None):
    def decorator(func):
        @wraps(func)
        @log_request
        @log_response
        @handle_exception
        @jwt_required_with_contact_and_role(allowed_roles=allowed_roles)
        def wrapper(*args, **kwargs):
            print("is in wrapper")
            return func(*args, **kwargs)
        return wrapper

    return decorator

def custom_jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):

        token = request.headers.get('Authorization')
        print("token",token)
        if not token:
            return jsonify({"error": "Token is missing!"})

        payload = decode_jwt(token)
        print("payload",payload)
        if not payload:
            return jsonify({"error": "Invalid or expired token!"})

        return fn(*args, **kwargs)

    return wrapper


def jwt_required_with_contact_validation(fn):
    @wraps(fn)
    @flask_jwt_required()
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"error": str(e)})

        contact_number = None
        if request.method == 'GET':
            # Get contact_number from query params in GET request
            contact_number = request.args.get('contact_number')
        elif request.method in ['POST', 'PUT', 'DELETE']:
            # Get contact_number from JSON body in other methods
            data = request.get_json()
            contact_number = data.get('contact_number')

        if not contact_number:
            return jsonify({"error": "Contact number is required."})

        # Get the user identity from JWT
        user_identity = get_jwt_identity()

        # Validate the contact_number matches the JWT identity
        if contact_number != user_identity:
            return jsonify({"error": "Invalid contact number."})

        return fn(*args, **kwargs)

    return wrapper


def jwt_required_with_contact_and_role(allowed_roles=None):
    """
    Decorator to ensure the request has a valid JWT with the contact number and role,
    and optionally restrict access to specific roles.
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Get JWT token from Authorization header
            auth_header = request.headers.get('Authorization', None)
            if not auth_header or not auth_header.startswith('Bearer '):
                return Response(json.dumps({"error": "Authorization token is required", "code": 401}), status=401)

            token = auth_header.split(" ")[1]
            role_header = request.headers.get('role')
            # Decode JWT
            decoded_response,decode_status = decode_jwt(token)

            # Extract contact_number and role from the token
            if decode_status != 200:
                return decoded_response

            contact_number = decoded_response.get('contact_number')
            role = decoded_response.get('role')

            if not contact_number or not role:
                return Response(json.dumps({"error": f"Invalid token payload", "code": 401}),status=401)
            print("role_header",role_header)
            if role != role_header:
                return Response(json.dumps({"error": f"Access denied for {role_header} as request is corrupted", "code": 401}), status=401)

            # Check if role is allowed (if specified)
            print("allowed_roles", allowed_roles)
            print("role", role_header)
            if allowed_roles and role_header not in allowed_roles:
                return Response(
                    json.dumps({"error": f"Access denied for role as {role_header}", "code": 401}),
                    status=401)
            return fn(*args, **kwargs)

        return wrapper

    return decorator