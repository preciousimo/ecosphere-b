from django.contrib import admin
from django.urls import path, include
from core.views import register_user, login_user, user_profile, verify_email
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('register/', register_user, name='register'),
        path('verify-email/<str:uidb64>/<str:token>/', verify_email, name='verify_email'),
        path('login/', login_user, name='login'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('profile/', user_profile, name='profile'),
        path('auth/', include('dj_rest_auth.urls')),
        path('auth/registration/', include('dj_rest_auth.registration.urls')),
        path('auth/google/', include('allauth.socialaccount.providers.google.urls')),
        path('auth/facebook/', include('allauth.socialaccount.providers.facebook.urls')),
    ])),
]