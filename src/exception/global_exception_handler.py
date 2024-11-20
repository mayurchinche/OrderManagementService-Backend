from functools import wraps

from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError


def handle_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ve:
            return jsonify({"error": "Value Error: " + str(ve)}), 400
        except TypeError as te:
            return jsonify({"error": "Type Error: " + str(te)}), 400
        except SQLAlchemyError as db_error:
            print(f"Database Error: {str(db_error)}")
            return jsonify({"error": "Database error occurred while registering user."}), 500
        except Exception as e:
            # Handle other exceptions
            return jsonify({"error": "An internal error occurred: " + str(e)}), 500

    return wrapper
