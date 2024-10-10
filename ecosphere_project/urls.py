from django.contrib import admin
from django.urls import path, include
from core.views import (
    user_profile,
    CommunityGardenListCreateView, CommunityGardenDetailView,
    SeasonalPlantingGuideListCreateView, SeasonalPlantingGuideDetailView,
    ProduceExchangeListingListCreateView, ProduceExchangeListingDetailView,
    GardeningTipListCreateView, GardeningTipDetailView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('userauth.urls')),
    path('api/', include('marketplace.urls')),
    path('api/', include('recycling.urls')),
    path('api/', include('energy_dashboard.urls')),
    path('api/', include([
        path('profile/', user_profile, name='profile'),

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
