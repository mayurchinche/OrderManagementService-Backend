import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from src.firebase import config as firebase_config

import json
firebase_credential_dict=firebase_config.get_credentials()
cred = credentials.Certificate(firebase_credential_dict)
firebase_admin.initialize_app(cred)

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
            description: Invalid token
        """
    try:
        # Verify the Firebase ID token
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token.get('uid')
        return user_id
    except Exception as e:
        raise ValueError(f"Token verification failed: {str(e)}")



import requests
import json

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
