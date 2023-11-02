from .models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=128)
    birth_date = serializers.DateField()
    city = serializers.CharField(max_length=50)
    province = serializers.CharField(max_length=30)
    gender = serializers.CharField(max_length=1)
    phone_number = serializers.CharField(max_length=15)
    account_type = serializers.CharField(max_length=2)
    
    occupancy = serializers.CharField(max_length=32, required=False)
    interest = serializers.CharField(max_length=32, required=False)
    motivation = serializers.CharField(required=False)

    company_name = serializers.CharField(max_length=64, required=False)
    company_address = serializers.CharField(max_length=255, required=False)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)

class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "profile_picture"]

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username

        return token