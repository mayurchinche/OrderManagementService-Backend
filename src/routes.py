import traceback

from flask import Blueprint, jsonify
from .db.db import db
from flasgger import swag_from
from sqlalchemy import text

main_routes = Blueprint("src", __name__)


@main_routes.route("/health", methods=["GET"])
def health_check():
    """
    Gives the system healthyness

    ---

    tags:
        - HealthCheck

    responses:
        200:
            description: Success
        500:
            description: Failure
    """
    print("System is healthy!..")
    return jsonify({"status": "OK"})


@main_routes.route("/test-db-connection", methods=["GET"])
def test_db_connection():
    """
    Test the database connection
    ---
    tags:
      - HealthCheck
    responses:
      200:
        description: Success
      500:
        description: Failure
    """
    try:
        print("Is in test Db")
        # Test a simple query to check the database connection
        print(
            db.session.execute(text("show tables"))
        )  # This is just to test the connection
        return jsonify({"message": "Database connection is successful!"}), 200
    except Exception as e:
        print("Exception as ex", e, traceback.print_exc())
        return jsonify({"error": str(e)}), 500
