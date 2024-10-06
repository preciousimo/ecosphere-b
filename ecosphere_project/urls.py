from django.contrib import admin
from django.urls import path, include
from core.views import (
    register_user, login_user, user_profile, verify_email,
    password_reset_request, password_reset_confirm,
    ResourceListCreateView, ResourceDetailView,
    BookingListCreateView, ReviewListCreateView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('register/', register_user, name='register'),
        path('verify-email/<str:uidb64>/<str:token>/', verify_email, name='verify_email'),
        path('password-reset/', password_reset_request, name='password_reset_request'),
        path('password-reset-confirm/<str:uidb64>/<str:token>/', password_reset_confirm, name='password_reset_confirm'),
        path('login/', login_user, name='login'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('profile/', user_profile, name='profile'),

        # Resource Sharing Marketplace URLs
        path('resources/', ResourceListCreateView.as_view(), name='resource_list_create'),
        path('resources/<int:pk>/', ResourceDetailView.as_view(), name='resource_detail'),
        path('bookings/', BookingListCreateView.as_view(), name='booking_list_create'),
        path('reviews/<int:resource_id>/', ReviewListCreateView.as_view(), name='review_list_create'),

        # Authentication and Social Auth
        path('auth/', include('dj_rest_auth.urls')),
        path('auth/registration/', include('dj_rest_auth.registration.urls')),
        path('auth/google/', include('allauth.socialaccount.providers.google.urls')),
        path('auth/facebook/', include('allauth.socialaccount.providers.facebook.urls')),
    ])),
]
