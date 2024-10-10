from django.urls import path, include
from energy_dashboard.views import (
    SmartHomeDeviceListCreateView, SmartHomeDeviceDetailView,
    EnergyUsageListCreateView, EnergySavingRecommendationListView,
    EnergySavingRecommendationMarkReadView, CommunityEnergyGoalListCreateView,
    CommunityEnergyGoalDetailView, UserCommunityProgressListView,
    UserCommunityProgressUpdateView, GenerateEnergySavingRecommendationsView,
)

urlpatterns = [
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
]
