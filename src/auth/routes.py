import sqlalchemy
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError

from src.auth.services import register_user, login_user

from werkzeug.security import generate_password_hash, check_password_hash

from src.logging.logging_handler import log_request
from src.models.user import User
from src.db.db import db
from src.sequrity.jwt_handler import encode_jwt
from src.exception.global_exception_handler import handle_exception
auth_bp = Blueprint('auth', __name__)


# Registration route
@log_request
@handle_exception
@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    ---
    tags:
      - Authentication
    parameters:
      - name: user
        in: body
        required: true
        schema:
          type: object
          properties:
            user_name:
              type: string
              example: "john_doe"
            password:
              type: string
              example: "securepassword"
            contact_number:
              type: string
              example: "1234567890"
    responses:
      201:
        description: User registered successfully
      400:
        description: Bad request
      409:
        description: User already exists
    """
    try:
        data = request.json
        print("Data", data)
        user_name = data.get('user_name')
        password = data.get('password')
        contact_number = data.get('contact_number')

        if not user_name or not password or not contact_number:
            return jsonify({"error": "Please provide user_name, password, and contact_number"}), 400

        # Check if user already exists
        existing_user = User.query.filter_by(user_name=user_name).first()
        if existing_user:
            return jsonify({"error": "User already exists"}), 409

        hashed_password = generate_password_hash(password)

        # Create a new user
        new_user = User(user_name=user_name, user_password=hashed_password, contact_number=contact_number)

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except SQLAlchemyError as e:
        db.session.rollback()  # Rollback in case of any error
        print(f"Database Error: {str(e)}")
        return jsonify({"error": "Database error occurred while registering user."}), 500
    except Exception as e:
        print(f"Unhandled Error: {str(e)}")
        return jsonify({"error": "An error occurred during registration."}), 500


# Login route
@log_request
@handle_exception
@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User Registration
            ---
            tags:
              - Authentication
            parameters:
              - in: body
                name: body
                schema:
                  type: object
                  required:
                    - contact_number
                    - password
                  properties:
                    contact_number:
                      type: string
                      description: The user's mobile number
                    password:
                      type: string
                      description: The user's password
            responses:
              200:
                description: Log In Successful
              401:
                description: User Not Found
    """
    try:

        # Get JSON data from the request
        data = request.get_json()
        print("Login request", request.get_json())
        contact_number = data.get('contact_number')
        password = data.get('password')

        if not contact_number or not password:
            return jsonify({"error": "Missing contact number or password!"}), 400

            # Query the database for the user
        user = db.session.query(User).filter_by(contact_number=contact_number).first()

        # Check if the provided password matches the stored password
        if not check_password_hash(user.user_password, password):
            return jsonify({"error": "Invalid password!"}), 401

        if not contact_number or not password:
            return jsonify({"error": "Missing contact number or password!"}), 400

        # Generate JWT token for the user
        token = encode_jwt(user)  # You might want to include user ID or other info in the token

        return jsonify({"message": "Login successful!", "token": token}), 200


    except SQLAlchemyError as e:

        print(f"Database Error: {str(e)}")

        return jsonify({"error": "Database error occurred while login user."}), 500

    except Exception as e:

        print(f"Unhandled Error: {str(e)}")

        return jsonify({"error": "User not found."}), 500
