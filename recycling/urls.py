from django.urls import path, include
from recycling.views import (
    WasteEntryListCreateView, RecyclingCenterListCreateView,
    RecyclingCenterDetailView, EcoChallengeListCreateView,
    EcoChallengeDetailView, UserChallengeListView,
    UserChallengeCompleteView, LeaderboardListView,
    UserWasteSummaryView, 
)

urlpatterns = [
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
]
