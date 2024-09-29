import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate('src/firebase/credentials.json')
firebase_admin.initialize_app(cred)



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
