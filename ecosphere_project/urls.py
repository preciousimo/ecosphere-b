from django.contrib import admin
from django.urls import path, include
from core.views import (
    register_user, login_user, user_profile, verify_email,
    password_reset_request, password_reset_confirm,
    ResourceListCreateView, ResourceDetailView,
    BookingListCreateView, ReviewListCreateView,
    WasteEntryListCreateView, RecyclingCenterListCreateView,
    RecyclingCenterDetailView, EcoChallengeListCreateView,
    EcoChallengeDetailView, UserChallengeListView,
    UserChallengeCompleteView, LeaderboardListView,
    UserWasteSummaryView, CreateCheckoutSessionView, stripe_webhook,
    SmartHomeDeviceListCreateView, SmartHomeDeviceDetailView,
    EnergyUsageListCreateView, EnergySavingRecommendationListView,
    EnergySavingRecommendationMarkReadView, CommunityEnergyGoalListCreateView,
    CommunityEnergyGoalDetailView, UserCommunityProgressListView,
    UserCommunityProgressUpdateView, GenerateEnergySavingRecommendationsView,
    CommunityGardenListCreateView, CommunityGardenDetailView,
    SeasonalPlantingGuideListCreateView, SeasonalPlantingGuideDetailView,
    ProduceExchangeListingListCreateView, ProduceExchangeListingDetailView,
    GardeningTipListCreateView, GardeningTipDetailView
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

        # Waste Reduction and Recycling URLs
        path('waste-entries/', WasteEntryListCreateView.as_view(), name='waste_entry_list_create'),
        path('recycling-centers/', RecyclingCenterListCreateView.as_view(), name='recycling_center_list_create'),
        path('recycling-centers/<int:pk>/', RecyclingCenterDetailView.as_view(), name='recycling_center_detail'),
        path('eco-challenges/', EcoChallengeListCreateView.as_view(), name='eco_challenge_list_create'),
        path('eco-challenges/<int:pk>/', EcoChallengeDetailView.as_view(), name='eco_challenge_detail'),
        path('user-challenges/', UserChallengeListView.as_view(), name='user_challenge_list'),
        path('user-challenges/complete/<int:challenge_id>/', UserChallengeCompleteView.as_view(), name='user_challenge_complete'),
        path('leaderboard/', LeaderboardListView.as_view(), name='leaderboard_list'),
        path('user-waste-summary/', UserWasteSummaryView.as_view(), name='user_waste_summary'),

        # Sustainable Energy Dashboard URLs
        path('smart-devices/', SmartHomeDeviceListCreateView.as_view(), name='smart_device_list_create'),
        path('smart-devices/<int:pk>/', SmartHomeDeviceDetailView.as_view(), name='smart_device_detail'),
        path('energy-usages/', EnergyUsageListCreateView.as_view(), name='energy_usage_list_create'),
        path('energy-recommendations/', EnergySavingRecommendationListView.as_view(), name='energy_recommendation_list'),
        path('energy-recommendations/mark-read/<int:recommendation_id>/', EnergySavingRecommendationMarkReadView.as_view(), name='energy_recommendation_mark_read'),
        path('community-energy-goals/', CommunityEnergyGoalListCreateView.as_view(), name='community_energy_goal_list_create'),
        path('community-energy-goals/<int:pk>/', CommunityEnergyGoalDetailView.as_view(), name='community_energy_goal_detail'),
        path('community-progress/', UserCommunityProgressListView.as_view(), name='user_community_progress_list'),
        path('community-progress/update/<int:community_goal_id>/', UserCommunityProgressUpdateView.as_view(), name='user_community_progress_update'),
        path('generate-recommendations/', GenerateEnergySavingRecommendationsView.as_view(), name='generate_energy_recommendations'),
        # Payment and Webhooks
        path('create-checkout-session/<int:resource_id>/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
        path('webhook/stripe/', stripe_webhook, name='stripe_webhook'),

        # Local Food Production URLs
        path('gardens/', CommunityGardenListCreateView.as_view(), name='community_garden_list_create'),
        path('gardens/<int:pk>/', CommunityGardenDetailView.as_view(), name='community_garden_detail'),
        path('seasonal-planting-guides/', SeasonalPlantingGuideListCreateView.as_view(), name='seasonal_planting_guide_list_create'),
        path('seasonal-planting-guides/<int:pk>/', SeasonalPlantingGuideDetailView.as_view(), name='seasonal_planting_guide_detail'),
        path('produce-exchange-listings/', ProduceExchangeListingListCreateView.as_view(), name='produce_exchange_listing_list_create'),
        path('produce-exchange-listings/<int:pk>/', ProduceExchangeListingDetailView.as_view(), name='produce_exchange_listing_detail'),
        path('gardening-tips/', GardeningTipListCreateView.as_view(), name='gardening_tip_list_create'),
        path('gardening-tips/<int:pk>/', GardeningTipDetailView.as_view(), name='gardening_tip_detail'),

        # Authentication and Social Auth
        path('auth/', include('dj_rest_auth.urls')),
        path('auth/registration/', include('dj_rest_auth.registration.urls')),
        path('auth/google/', include('allauth.socialaccount.providers.google.urls')),
        path('auth/facebook/', include('allauth.socialaccount.providers.facebook.urls')),
    ])),
]
