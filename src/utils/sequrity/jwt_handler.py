import os

import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask_jwt_extended import create_access_token, decode_token

secret_key = os.getenv("secret_key")


def encode_jwt(user):
    payload = {
        "sub": user.contact_number,  # This will act as the identity (subject) claim
        "exp": datetime.utcnow() + timedelta(days=1),  # Token expires in 1 day
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


def decode_jwt(token):
    try:
        payload = jwt.decode(token, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token


def create_jwt_token(identity):
    return create_access_token(identity=identity)


def decode_jwt(token):
    try:
        decoded = decode_token(token)
        return decoded
    except Exception as e:
        return None


def generate_token(user):
    token = create_access_token(
        identity=user.contact_number, additional_claims={"role": user.role}
    )
    return token
