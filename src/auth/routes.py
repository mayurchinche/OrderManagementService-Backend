import json

import sqlalchemy
from flask import Blueprint, request, jsonify, Response
from sqlalchemy.exc import SQLAlchemyError

from src.auth.services import register_user, login_user

from werkzeug.security import generate_password_hash, check_password_hash

from src.logging.logging_handler import log_request
from src.models.user import User
from src.db.db import db
from src.sequrity.jwt_handler import encode_jwt
from src.exception.global_exception_handler import handle_exception
from flask import request, jsonify
from firebase_admin import auth
from src.firebase import service as firebase_service

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
    responses:
      201:
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
              example: "User with this contact number already exists"
      401:
        description: "Invalid or expired Firebase token."
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid or expired Firebase token"
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
        print("Data", data)
        id_token = data.get('id_token')
        user_name = data.get('user_name')
        password = data.get('password')
        contact_number = data.get('contact_number')
        print(data)
        if not id_token or not user_name or not password or not contact_number:
            return jsonify({"error": "Please provide id_token, user_name, password, and contact_number"}), 400

        # Verify the Firebase id_token

        decoded_token, status_code=firebase_service.verify_firebase_token(id_token)

        if status_code==200:
            print(decoded_token.get_data(as_text=True), status_code)
            firebase_user_data=decoded_token.get_data(as_text=True)

            firebase_user_data_json=json.loads(firebase_user_data)


            print("firebase_user_data",firebase_user_data_json)

            firebase_contact_number=firebase_user_data_json.get("contact_number")
            print("firebase_contact_number",firebase_contact_number)
            # Ensure that the contact number matches the one in the Firebase token
            if contact_number != firebase_contact_number:
                return jsonify({"error": "Contact number does not match Firebase token"}), 400

            # Check if user already exists
            existing_user = User.query.filter_by(contact_number=contact_number).first()
            if existing_user:
                print("User already exists")
                return jsonify({"error": "User already exists"}), 409

            hashed_password = generate_password_hash(password)

            # Create a new user
            new_user = User(user_name=user_name, user_password=hashed_password, contact_number=contact_number)

            # Add the user to the database
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "User registered successfully!"}), 201
        else:
            print(decoded_token.get_data(as_text=True))
            return jsonify({"error": "Something Went Wrong."}), 400
    except SQLAlchemyError as e:
        db.session.rollback()  # Rollback in case of any error
        print(f"Database Error: {str(e)}")
        return jsonify({"error": "Database error occurred while registering user."}), 500
    except Exception as e:
        print(f"Unhandled Error: {str(e)}")
        return jsonify({"error": "An error occurred during registration."}), 500

@log_request
@handle_exception
@auth_bp.route('/generate_token', methods=['POST'])
def generate_token():
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
@log_request
@handle_exception
@auth_bp.route('/login', methods=['POST'])
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


def is_otp_verified(contact_number):
    # Implement your logic to verify if OTP was confirmed for the contact number
    # This might involve checking a database record or in-memory store
    return True  # Placeholder; replace with actual verification logic











# @log_request
# @handle_exception
# @auth_bp.route('/send-otp', methods=['POST'])
# def send_otp():
#     """
#     Send an OTP to the user's contact number
#     ---
#     tags:
#       - Authentication
#     parameters:
#       - in: body
#         name: body
#         required: true
#         description: JSON payload with contact_number
#         schema:
#           type: object
#           required:
#             - contact_number
#           properties:
#             contact_number:
#               type: string
#               description: The contact number to send the OTP to.
#     responses:
#       200:
#         description: OTP sent successfully
#         schema:
#           type: object
#           properties:
#             message:
#               type: string
#             otp:
#               type: string
#             contact_number:
#               type: string
#       400:
#         description: Invalid contact number format
#         schema:
#           type: object
#           properties:
#             error:
#               type: string
#     """
#     data = request.json
#     contact_number = data.get('contact_number')
#
#     try:
#         if not contact_number:
#             return jsonify({'error': 'Contact number is required'}), 400
#
#             # Call function to send OTP
#         token = firebase_config.firebase_send_otp(contact_number)
#
#         if token:
#             return jsonify({'message': 'OTP sent', 'token': token}), 200
#         else:
#             return jsonify({'error': 'Failed to send OTP'}), 500
#
#     except Exception as ex:
#         return jsonify({"error": str(ex)}), 500
#
#     # print("contact_number: ",contact_number)
#     # # Use Firebase to send OTP
#     # try:
#     #     verification_id = auth.verify_id_token(contact_number)  # Adjust according to your Firebase implementation
#     #     print("verification_id",verification_id)
#     #     # Send OTP logic here (Firebase will handle it)
#     #     return jsonify({"message": "OTP sent successfully!", "contact_number":contact_number,"verification_id": verification_id}), 200
#     # except Exception as e:
#     #     return jsonify({"error": str(e)}), 500

# @log_request
# @handle_exception
# @auth_bp.route('/verify_user', methods=['POST'])
# def verify_user():
#     try:
#         # Get Firebase ID token from request headers
#         id_token = request.headers.get('Authorization').split(" ")[1]  # Assuming 'Bearer <token>'
#
#         # Verify the token
#         user_id = firebase_service.verify_firebase_token(id_token)
#
#         # Return success response if token is valid
#         return jsonify({"message": "User verified successfully", "user_id": user_id}), 200
#     except ValueError as e:
#         return jsonify({"error": str(e)}), 400