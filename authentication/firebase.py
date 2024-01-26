import os
from django.db import IntegrityError
import firebase_admin
from django.conf import settings
from apps.accounts.models import CustomUser
from django.utils import timezone
from firebase_admin import auth
from firebase_admin import credentials
from rest_framework import authentication
from rest_framework import exceptions
from .exceptions import ExpiredAuthToken, FirebaseError, UserAlreadyRegistered
from .exceptions import InvalidAuthToken
from .exceptions import NoAuthToken
# from decouple import config

# cred = credentials.Certificate({
#         "type": "service_account",
#         "project_id": config('FIREBASE_PROJECT_ID'),
#         "private_key_id": config('FIREBASE_PRIVATE_KEY_ID'),
#         "private_key": config('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
#         "client_email": config('FIREBASE_CLIENT_EMAIL'),
#         "client_id": config('FIREBASE_CLIENT_ID'),
#         "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#         "token_uri": "https://oauth2.googleapis.com/token",
#         "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#         "client_x509_cert_url": config('FIREBASE_CLIENT_CERT_URL')
#     })

# default_app = firebase_admin.initialize_app(cred)


# # config = {
# #   "apiKey": "4c12ece798f20587c6eda7e9dde35343a0ad2e43",
# #   "authDomain": "islamicbot-devl.firebaseapp.com",
# #   "databaseURL": "https://databaseName.firebaseio.com",
# #   "storageBucket": "islamicbot-devl.appspot.com",
# #   "serviceAccount": cred
# # }

# # firebase = pyrebase.initialize_app(config)
# """
# If your Firebase client app communicates with a custom backend server, 
# you might need to identify the currently signed-in user on that server. 
# To do so securely, after a successful sign-in, send the user's ID token 
# to your server using HTTPS.

# https://firebase.google.com/docs/auth/admin/verify-id-tokens
# """

# class  FirebaseRegisterAuthentication(authentication.BaseAuthentication):

#     def authenticate(self, request):
#         auth_header = request.META.get("HTTP_AUTHORIZATION")
#         if not auth_header:
#             raise NoAuthToken("No auth token provided")

#         id_token = auth_header.split(" ").pop()
#         decoded_token = None
#         try:
#             decoded_token = auth.verify_id_token(id_token)  
#         except Exception:
#             raise InvalidAuthToken("Invalid/expired a auth token")

#         if not id_token or not decoded_token:
#             return None
#         try:
#             uid = decoded_token.get("uid")
#         except Exception:
#             raise FirebaseError()
#         try:
#             user = CustomUser.objects.create(uid=uid, email=uid+"@placeholder.com")
#         except IntegrityError as e:
#             user = CustomUser.objects.get(uid=uid)
#             user.last_login = timezone.localtime()
#             print(user)
#             if request.method == "POST":
#                 response = {
#                 "status":400,
#                 "msg":"User Already registered"
#                 }
#                 raise UserAlreadyRegistered(response)

#             else:
#                 return (user, None)
                
#         user.last_login = timezone.localtime()
#         return (user, None)

#     def get_uid_from_token(self, request):
#         auth_header = request.META.get("HTTP_AUTHORIZATION")
#         uid = auth_header.split(" ").pop()
#         decoded_token = auth.verify_id_token(uid)
#         uid = decoded_token.get('uid')

#         return uid         
    

class FirebaseAuthentication(authentication.BaseAuthentication):
    
    def authenticate(self, request):
        # auth_header = request.META.get("HTTP_AUTHORIZATION")
  
        # if not auth_header:
        #     raise NoAuthToken("No auth token provided")

        # id_token = auth_header.split(" ").pop()
        # decoded_token = None

        # try:
        #     decoded_token = auth.verify_id_token(id_token)            
        # except Exception:
        #     raise InvalidAuthToken("Invalid/expired auth token")

        # if not id_token or not decoded_token:
        #     return None

        try:
            uid = "aaa0000"
            # uid = decoded_token.get("uid")
        except Exception:
            raise FirebaseError()
        try:
            user = CustomUser.objects.get(uid=uid)
            user.last_login = timezone.localtime()
        except Exception:
            raise InvalidAuthToken("Please register this token first @ /api/v1/accounts/user/register/")
        return (user, uid)

    def authenticate_v2(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
  
        if not auth_header:
            raise NoAuthToken("No auth token provided")

        id_token = auth_header.split(" ").pop()
        decoded_token = None

        try:
            decoded_token = auth.verify_id_token(id_token)            
        except Exception:
            raise InvalidAuthToken("Invalid/expired auth token")

        if not id_token or not decoded_token:
            return None

        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise FirebaseError()
        try:
            user = CustomUser.objects.get(uid=uid)
            user.last_login = timezone.localtime()
            return True
        except Exception:
            raise InvalidAuthToken("Please register this token first @ /api/v1/accounts/user/register/")
        
        return False

    
    def get_user_by_email(self,email):
        try:
            return firebase_admin.auth.get_user_by_email(email)

        except:
            return None
    
    
    def get_uid_from_token(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        uid = auth_header.split(" ").pop()
        decoded_token = auth.verify_id_token(uid)
        uid = decoded_token.get('uid')

        return uid  
     
    def get_user_from_token(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        uid = auth_header.split(" ").pop()
        decoded_token = auth.verify_id_token(uid)
        uid = decoded_token.get('uid')
        try:
            user = CustomUser.objects.get(uid=uid)
        except:
            raise InvalidAuthToken("Please register this token first @ /api/v1/accounts/user/register/")

        return user 
      
    def get_user_from_auth_token(self, auth_token):
        uid = auth_token.split(" ").pop()
        decoded_token = auth.verify_id_token(uid)
        uid = decoded_token.get('uid')
        print(uid)
        # uid = "3O7tSphxWRVUpwIjgC8hhWZnPXD3"
        try:
            user = CustomUser.objects.get(uid=uid)
        except:
            raise InvalidAuthToken("Please register this token first @ /api/v1/accounts/user/register/")

        return user   
