import json
import traceback
from datetime import datetime, timedelta

import jwt
from firebase_admin import auth
from flask import Blueprint
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

from src.db.db import db
from src.exception.global_exception_handler import handle_exception
from src.firebase import service as firebase_service
from src.logging.logging_handler import log_request, log_response
from src.models.users import User
from src.sequrity.decorators import jwt_required_with_contact_validation
from src.sequrity.jwt_handler import encode_jwt
from src.sequrity.jwt_handler import secret_key

auth_bp = Blueprint('auth', __name__)


# Registration route

@auth_bp.route('/register', methods=['POST'])
@log_request
@log_response
@handle_exception
def register():
    """
    Register a new user.

    ---
    tags:
      - UserRegistration
    summary: "Register a new user"
    description: "This endpoint registers a new user after verifying the OTP using Firebase authentication."
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        description: JSON payload containing user registration data.
        schema:
          type: object
          required:
            - id_token
            - user_name
            - password
            - contact_number
            - role
          properties:
            id_token:
              type: string
              description: "The Firebase ID token received after OTP verification."
            user_name:
              type: string
              description: "The user's name."
            password:
              type: string
              description: "The user's password (will be hashed before storing)."
            contact_number:
              type: string
              description: "The user's contact number (phone number)."
            role:
              type: string
              description: "The user's role."

    responses:
      200:
        description: "User registered successfully."
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User registered successfully!"
      400:
        description: "Missing required fields or validation errors."
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Please provide id_token, user_name, password, and contact_number"
      401:
        description: "Contact number does not match Firebase token or Invalid or expired Firebase token."
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid or expired Firebase token"
      409:
        description: "User already exists."
        schema:
          type: object
          properties:
            error:
              type: string
              example: "User already exists"
      500:
        description: "Internal server error or database issues."
        schema:
          type: object
          properties:
            error:
              type: string
              example: "An internal error occurred. Please try again later."
    """
    try:
        data = request.json
        id_token = data.get('id_token')
        user_name = data.get('user_name')
        password = data.get('password')
        contact_number = data.get('contact_number')
        if not id_token or not user_name or not password or not contact_number:
            return jsonify({"error": "Please provide id_token, user_name, password, and contact_number"}), 400

        # Verify the Firebase id_token

        decoded_token, status_code = firebase_service.verify_firebase_token(id_token)

        if status_code == 200:
            firebase_user_data = decoded_token.get_data(as_text=True)

            firebase_user_data_json = json.loads(firebase_user_data)

            firebase_contact_number = firebase_user_data_json.get("contact_number")

            # Ensure that the contact number matches the one in the Firebase token
            if contact_number != firebase_contact_number:
                return jsonify({"error": "Contact number does not match Firebase token"}), 401

            # Check if user already exists
            existing_user = User.query.filter_by(contact_number=contact_number).first()
            if existing_user:
                return jsonify({"error": "User already exists"}), 409

            hashed_password = generate_password_hash(password)

            # Create a new user
            new_user = User(user_name=user_name, user_password=hashed_password, contact_number=contact_number,role=role)

            print("New User", new_user)
            # Add the user to the database
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "User registered successfully!"}), 200
        else:
            return jsonify({"error": "Something Went Wrong."}), 500
    except SQLAlchemyError as e:
        print("SQLAlchemyError", traceback.print_exc())
        db.session.rollback()  # Rollback in case of any error
        return jsonify({"error": "Database error occurred while registering user."}), 500
    except Exception as e:
        return jsonify({"error": "An error occurred during registration."}), 500


@auth_bp.route('/generate_firebase_token', methods=['POST'])
@log_request
@log_response
@handle_exception
def generate_firebase_token():
    """
    Generate a Firebase custom token for a user.

    ---
    tags:
      - UserRegistration
    summary: "Generate Firebase token"
    description: "This endpoint generates a Firebase custom token for a user after verifying the OTP."
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        description: JSON payload containing user details.
        schema:
          type: object
          required:
            - contact_number
          properties:
            contact_number:
              type: string
              description: "The user's contact number."
    responses:
      200:
        description: "Token generated successfully."
        schema:
          type: object
          properties:
            token:
              type: string
              description: "Firebase custom token."
      400:
        description: "Missing required fields or OTP not verified."
        schema:
          type: object
          properties:
            error:
              type: string
              example: "OTP not verified or invalid contact number."
      500:
        description: "Internal server error."
        schema:
          type: object
          properties:
            error:
              type: string
              example: "An internal error occurred. Please try again later."
    """
    data = request.get_json()
    contact_number = data.get('contact_number')

    if not contact_number:
        return jsonify({"error": "Contact number is required."}), 400

    try:
        # Check if OTP has been verified (implement your own logic here)
        if not is_otp_verified(contact_number):  # Placeholder function
            return jsonify({"error": "OTP not verified."}), 400

        # Generate custom token
        custom_token = auth.create_custom_token(contact_number)

        return jsonify({"token": custom_token.decode()}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Login route

@auth_bp.route('/login', methods=['POST'])
@log_request
@log_response
@handle_exception
def login():
    """
    User Authentication
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
                description: Login successful!
              401:
                description: Invalid password, Please try again!
              404:
                description: User not found, Please Sign up First !
              500:
                description: Database error occurred while login user. OR Somthing went wrong


    """
    try:

        # Get JSON data from the request
        data = request.get_json()
        contact_number = data.get('contact_number')
        password = data.get('password')
        # Query the database for the user
        user = db.session.query(User).filter_by(contact_number=contact_number).first()

        if user is None:
            # user not found
            return jsonify({"error": "User not found, Please Sign up First !"}), 404
        # Check if the provided password matches the stored password
        if not check_password_hash(user.user_password, password):
            return jsonify({"error": "Invalid password, Please try again!"}), 401

        # Generate JWT token for the user
        token = encode_jwt(user)  # You might want to include user ID or other info in the token
        return jsonify({"message": "Login successful!", "token": token}), 200


    except SQLAlchemyError as e:

        return jsonify({"error": "Database error occurred while login user."}), 500

    except Exception as e:
        return jsonify({"error": f"Something went wrong, {e} {traceback.print_exc()}"}), 500


def is_otp_verified(contact_number):
    # Implement your logic to verify if OTP was confirmed for the contact number
    # This might involve checking a database record or in-memory store
    return True  # Placeholder; replace with actual verification logic


@auth_bp.route('/generate_jwt_token', methods=['POST'])
@log_request
@log_response
def generate_jwt_token():
    """
        Generate a JWT custom token for a user.

        ---
        tags:
            - Authentication
        summary: "Generate JWT token"
        description: "This endpoint generates a JWT custom token for a user after login."
        consumes:
          - application/json
        produces:
          - application/json
        parameters:
          - in: body
            name: body
            required: true
            description: JSON payload containing user details.
            schema:
              type: object
              required:
                - contact_number
              properties:
                contact_number:
                  type: string
                  description: "The user's contact number."
        responses:
          200:
            description: "Token generated successfully."
            schema:
              type: object
              properties:
                token:
                  type: string
                  description: "JWT custom token."
          400:
            description: "Missing required fields or OTP not verified."
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "OTP not verified or invalid contact number."
          500:
            description: "Internal server error."
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "An internal error occurred. Please try again later."
        """
    data = request.get_json()
    print("data", data)
    contact_number = data.get('contact_number')
    if not contact_number or not isinstance(contact_number, str):
        return jsonify({"error": "Contact number is required and must be a string."}), 400

    try:

        payload = {'sub': contact_number,  # This will act as the identity (subject) claim
            'exp': datetime.utcnow() + timedelta(days=1)  # Token expires in 1 day
        }

        # Encode the payload into a JWT using the secret key
        encoded_token = jwt.encode(payload, secret_key, algorithm='HS256')

        return jsonify({"token": encoded_token}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@log_response
@auth_bp.route('/protected', methods=['POST'])
@jwt_required_with_contact_validation
def protected():
    """
        Validate JWT and contact number.

        ---
        tags:
          - Protected
        summary: "Access protected route"
        description: "This endpoint allows access only to users with a valid JWT token and a matching contact number in the request body."
        consumes:
          - application/json
        produces:
          - application/json
        parameters:
          - in: header
            name: Authorization
            required: true
            description: "JWT Token in Bearer format"
            schema:
              type: string
          - in: body
            name: body
            description: JSON payload with contact number.
            schema:
              type: object
              required:
                - contact_number
              properties:
                contact_number:
                  type: string
                  description: "User's contact number"
                other_data:
                  type: string
                  description: "Additional data"
        responses:
          200:
            description: "Protected route access granted"
            schema:
              type: object
              properties:
                message:
                  type: string
                contact_number:
                  type: string
                data:
                  type: object
          401:
            description: "Invalid token or contact number mismatch"
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Invalid contact number"
          500:
            description: "Internal server error"
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "An internal error occurred."
        """
    jwt_contact_number = get_jwt_identity()  # The contact number from the JWT
    data = request.get_json()  # The request body
    # Additional logic to process the request

    return jsonify(
        {"message": "Protected route access granted", "contact_number": jwt_contact_number, "data": data}), 200
