from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.permissions import IsAuthenticated
from .models import User, BlacklistedToken, CompanyAccount, PersonalAccount
from .serializers import *
from .wrapper import validate_serializer
from rest_framework import status

@api_view(["POST"])
@validate_serializer(RegisterSerializer)
def register(request, data):
    hash_password = make_password(data["password"])
    user = User(email=data["email"], password=hash_password, username=data["username"], birth_date=data["birth_date"], city=data["city"], province=data["province"], gender=data["gender"], phone_number=data["phone_number"], account_type=data["account_type"])
    if not (User.objects.filter(email=data["email"]).exists()):
        user.save()
        if (data["account_type"] == "PR"):
            personal_account = PersonalAccount(id=user, occupancy=data["occupancy"], occupancy_info=data["occupancy_info"], interest=data["interest"], motivation=data["motivation"])
            personal_account.save()
        else:
            company_account = CompanyAccount(id=user, name=data["company_name"], address=data["company_address"])
            company_account.save()
        return JsonResponse({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse({"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["POST"])
@validate_serializer(LoginSerializer)
def login(request, data):
    user = User.objects.filter(email=data["email"])
    if(not user):
        return JsonResponse({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    user = authenticate(request, email=data["email"], password=data["password"])
    if user is not None:
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return JsonResponse({"refreshToken": str(refresh), "accessToken": str(access)}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"message": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
@validate_serializer(LogoutSerializer)
@permission_classes([IsAuthenticated])
def logout(request, data):
    try:
        token = request.data['token']
        refresh_token = RefreshToken(token)
        refresh_token.blacklist()
        BlacklistedToken.objects.create(token=token)
        return JsonResponse({'message': 'Logout successful'}, status=status.HTTP_205_RESET_CONTENT)
    except TokenError as e:
        return JsonResponse({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    data = UserSerializer(user).data
    return JsonResponse(data, status=status.HTTP_200_OK)