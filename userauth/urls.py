from django.urls import path, include
from userauth.views import (
    register_user, login_user, verify_email,
    password_reset_request, password_reset_confirm,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
        path('register/', register_user, name='register'),
        path('verify-email/<str:uidb64>/<str:token>/', verify_email, name='verify_email'),
        path('password-reset/', password_reset_request, name='password_reset_request'),
        path('password-reset-confirm/<str:uidb64>/<str:token>/', password_reset_confirm, name='password_reset_confirm'),
        path('login/', login_user, name='login'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

        # Authentication and Social Auth
        path('auth/', include('dj_rest_auth.urls')),
        path('auth/registration/', include('dj_rest_auth.registration.urls')),
        path('auth/google/', include('allauth.socialaccount.providers.google.urls')),
        path('auth/facebook/', include('allauth.socialaccount.providers.facebook.urls')),
]
