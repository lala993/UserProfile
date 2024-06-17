import firebase_admin
from firebase_admin import auth, credentials
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from google.oauth2 import service_account
import logging
import os
logger = logging.getLogger(__name__)



# serviceAccount_path = service_account.Credentials.from_service_account_file(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
serviceAccount_path = r"D:\my_projects\firebase-auth\UserProfile\serviceAccounts\serviceAccountKey.json"
cred = credentials.Certificate(serviceAccount_path)
firebase_admin.initialize_app(cred)

class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        id_token = auth_header.split(' ').pop()
        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
        except Exception as e:
            raise AuthenticationFailed('Invalid token.')

        return (uid, None)
