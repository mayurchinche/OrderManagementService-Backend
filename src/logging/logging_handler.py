import json

from flask import Flask, jsonify, request
from functools import wraps
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Decorator for logging requests
def log_request(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.method != 'GET':
            if not request.is_json:
                return jsonify({"error": "Request must be JSON"}), 415
            data = request.get_json()
            print(f"Request: {request.url} \nRequest data: {data}")
        else:
            print(f"GET request for {request.url} received with params: {request.args}")
        return f(*args, **kwargs)

    return wrapper


def log_response(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        response = f(*args, **kwargs)
        if isinstance(response, tuple):
            response_json, status_code = response
            logger.info(f"Response sent: {status_code} {json.dumps(response_json)}")
        else:
            # Assume it's a Flask Response object
            logger.info(f"Response sent: {response.status_code} {response.data}")
        return response

    return wrapper
