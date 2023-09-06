from rest_framework import serializers
from account.models import *
# from firebase_auth.authentication import FirebaseRegisterAuthentication
from firebase_admin import auth

class UserSerializer_v2(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('uid', 'email', 'is_email_verified', 'first_name', 'last_name')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
        # fields = ('uid', 'email', 'is_email_verified', 'first_name', 'last_name', 'date_of_birth', 'created_on', 'updated_on')
        # fields = ('uid', 'email', 'is_email_verified', 'first_name', 'last_name', 'date_of_birth', 'created_on', 'updated_on')
