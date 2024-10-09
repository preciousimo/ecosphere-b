from django.contrib import admin
from django.urls import path, include
from core.views import (
    user_profile,
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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('userauth.urls')),
    path('api/', include('marketplace.urls')),
    path('api/', include([
        path('profile/', user_profile, name='profile'),

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

        # Local Food Production URLs
        path('gardens/', CommunityGardenListCreateView.as_view(), name='community_garden_list_create'),
        path('gardens/<int:pk>/', CommunityGardenDetailView.as_view(), name='community_garden_detail'),
        path('seasonal-planting-guides/', SeasonalPlantingGuideListCreateView.as_view(), name='seasonal_planting_guide_list_create'),
        path('seasonal-planting-guides/<int:pk>/', SeasonalPlantingGuideDetailView.as_view(), name='seasonal_planting_guide_detail'),
        path('produce-exchange-listings/', ProduceExchangeListingListCreateView.as_view(), name='produce_exchange_listing_list_create'),
        path('produce-exchange-listings/<int:pk>/', ProduceExchangeListingDetailView.as_view(), name='produce_exchange_listing_detail'),
        path('gardening-tips/', GardeningTipListCreateView.as_view(), name='gardening_tip_list_create'),
        path('gardening-tips/<int:pk>/', GardeningTipDetailView.as_view(), name='gardening_tip_detail'),
    ])),
]
