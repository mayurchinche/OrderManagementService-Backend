import traceback
from functools import wraps
import json
from flask import jsonify, Response
from sqlalchemy.exc import SQLAlchemyError

from src.logging.logging_handler import log_response

def handle_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            print(traceback.print_exc())
            try:
                raise
            except ValueError as ve:
                return Response(json.dumps({"error": "Value Error: " + str(ve), "code": 400}), status=400)
            except TypeError as te:
                return Response(json.dumps({"error":  "Type Error: " + str(te), "code": 400}), status=400)
            except SQLAlchemyError as db_error:
                return Response(json.dumps({"error": "Database error occurred", "code": 500}), status=500)
            except Exception as e:
                return Response(json.dumps({"error":"An internal error occurred: " + str(e), "code": 500}), status=500)

    return wrapper