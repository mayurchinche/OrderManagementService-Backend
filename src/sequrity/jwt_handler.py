import jwt
from datetime import datetime, timedelta

secret_key = "your_secret_key"  # Store this in an env variable

def create_jwt(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=1)  # Token expires in 1 day
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

def decode_jwt(token):
    try:
        payload = jwt.decode(token, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token