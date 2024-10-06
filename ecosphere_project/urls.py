from django.contrib import admin
from django.urls import path, include
from core.views import register_user, login_user, user_profile
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('register/', register_user, name='register'),
        path('login/', login_user, name='login'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('profile/', user_profile, name='profile'),
    ])),
]