import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from flask import jsonify

from src.exception.global_exception_handler import handle_exception
from src.firebase import config as firebase_config

import requests
import json

from src.logging.logging_handler import log_request

firebase_credential_dict=firebase_config.get_credentials()
cred = credentials.Certificate(firebase_credential_dict)
firebase_admin.initialize_app(cred)
FIREBASE_API_KEY="AIzaSyBHqA9lD6ynLsb0C35tn7XQM1F7LzAgA9U"
@log_request
@handle_exception
def verify_firebase_token(id_token):
    """
        Verify Firebase Token
        ---
        tags:
          - Authentication
        parameters:
          - name: Authorization
            in: header
            type: string
            required: true
            description: "Bearer <Firebase ID Token>"
        responses:
          200:
            description: User verified successfully
          400:
            description: Invalid token/ or some other exception
        """
    try:
        # Verify the Firebase ID token
        decoded_token = auth.verify_id_token(id_token)
        print("decoded_token--service: ",decoded_token)

        firebase_user_id = decoded_token['uid']
        firebase_contact_number = decoded_token.get('phone_number')
        # Proceed with further registration logic, e.g., saving the user to your database
        return jsonify({
            "message": "User registered successfully!",
            "uid": firebase_user_id,
            "contact_number": firebase_contact_number
        }), 200

    except Exception as e:
        # Handle error if token verification fails
        return jsonify({"error": str(e)}), 400

@log_request
@handle_exception
def exchange_custom_token_for_id_token(custom_token):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={FIREBASE_API_KEY}"

    payload = {
        "token": custom_token.decode(),
        "returnSecureToken": True
    }

    headers = {
        "Content-Type": "application/json"
    }

    print("Hittting",payload)

    response = requests.post(url, data=json.dumps(payload))

    print("Repsonse", response.text)

    if response.status_code == 200:
        print("Got succcessful response")
        id_token = response.json().get('idToken')
        print("id_token", id_token)
        return id_token
    else:
        raise Exception(f"Failed to exchange custom token: {response.text}")


# FIREBASE_API_KEY = 'your-firebase-api-key'


# def firebase_send_otp(contact_number):
#     url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendVerificationCode?key={FIREBASE_API_KEY}"
#     payload = {
#         "phoneNumber": contact_number,
#         "recaptchaToken": "your-recaptcha-token"  # You'll need to handle recaptcha as part of this
#     }
#
#     headers = {
#         "Content-Type": "application/json"
#     }
#
#     try:
#         response = requests.post(url, data=json.dumps(payload), headers=headers)
#         response_data = response.json()
#         if 'sessionInfo' in response_data:
#             return response_data['sessionInfo']  # sessionInfo is needed to verify OTP
#         else:
#             return response_data.get('error', 'Unknown error occurred')
#     except Exception as e:
#         return str(e)
#
#
# def firebse_verify_otp(contact_number, otp, session_info):
#     url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPhoneNumber?key={FIREBASE_API_KEY}"
#     payload = {
#         "sessionInfo": session_info,
#         "code": otp
#     }
#
#     headers = {
#         "Content-Type": "application/json"
#     }
#
#     try:
#         response = requests.post(url, data=json.dumps(payload), headers=headers)
#         response_data = response.json()
#         if 'idToken' in response_data:
#             return response_data['idToken']  # The token can be used for authenticated requests
#         else:
#             return response_data.get('error', 'Unknown error occurred')
#     except Exception as e:
#         return str(e)
