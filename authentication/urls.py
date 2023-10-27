from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('logout', logout, name='logout'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('get-user-info', get_user_info, name='get_user_info'),
]