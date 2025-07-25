from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, 
    CustomTokenObtainPairView, 
    UserProfileView,
    user_info,
    change_password,
    check_email_availability,
    check_username_availability
)

app_name = 'users'

urlpatterns = [
    # Authentication endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Profile management endpoints
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('info/', user_info, name='user_info'),
    path('change-password/', change_password, name='change_password'),
    
    # Utility endpoints
    path('check-email/', check_email_availability, name='check_email'),
    path('check-username/', check_username_availability, name='check_username'),
]
