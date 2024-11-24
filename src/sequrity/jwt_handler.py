import os
import jwt
from datetime import datetime, timedelta
from flask import jsonify
from flask_jwt_extended import create_access_token
from src.exception.global_exception_handler import handle_exception


secret_key=os.getenv('secret_key')
@handle_exception
def encode_jwt(user):

    payload = {
        'contact_number': user.contact_number,   # This will act as the identity (subject) claim
        'role': user.role,
        'exp': datetime.utcnow() + timedelta(days=1)  # Token expires in 1 day
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token


@handle_exception
def decode_jwt(token):
    try:
        payload = jwt.decode(token, secret_key,algorithms=['HS256'])
        return payload, 200
    except jwt.InvalidSignatureError:
        return {"error": "Invalid signature", "code": "401"},401  # Invalid signature
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired", "code": "401"},401  # Token has expired
    except jwt.InvalidTokenError:
        return {"error": "Invalid token", "code": "401"},401  # Invalid token

@handle_exception
def create_jwt_token(identity,role):
    return create_access_token(identity=identity, additional_claims={'role': role})

# def decode_jwt(token):
#     try:
#         decoded = decode_token(token)
#         return decoded
#     except Exception as e:
#         return None