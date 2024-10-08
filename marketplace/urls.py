from django.urls import path, include
from marketplace.views import (
    ResourceListCreateView, ResourceDetailView,
    BookingListCreateView, ReviewListCreateView,
    CreateCheckoutSessionView, stripe_webhook,
)

urlpatterns = [
        # Resource Sharing Marketplace URLs
        path('resources/', ResourceListCreateView.as_view(), name='resource_list_create'),
        path('resources/<int:pk>/', ResourceDetailView.as_view(), name='resource_detail'),
        path('bookings/', BookingListCreateView.as_view(), name='booking_list_create'),
        path('reviews/<int:resource_id>/', ReviewListCreateView.as_view(), name='review_list_create'),
        
        # Payment and Webhooks
        path('create-checkout-session/<int:resource_id>/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
        path('webhook/stripe/', stripe_webhook, name='stripe_webhook'),
]
