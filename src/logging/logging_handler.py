from flask import Flask, jsonify, request
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Decorator for logging requests
def log_request(f):
    def wrapper(*args, **kwargs):
        logger.info(f"Request received: {request.method} {request.url}")
        return f(*args, **kwargs)
    return wrapper
