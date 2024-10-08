from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from marketplace.models import (
    Resource, Booking, Review
)
from marketplace.serializers import (
    ResourceSerializer, BookingSerializer, ReviewSerializer,
)
from core.permissions import (
    IsAdminOrModerator, IsOwnerOrReadOnly
)
import logging
import stripe

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY

class ResourceListCreateView(generics.ListCreateAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description', 'category']
    filterset_fields = ['category', 'available']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ResourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [IsOwnerOrReadOnly | IsAdminOrModerator]

class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        resource_id = self.request.data.get('resource_id')
        resource = Resource.objects.get(id=resource_id)
        serializer.save(user=self.request.user, resource=resource)

class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        resource_id = self.kwargs['resource_id']
        return Review.objects.filter(resource__id=resource_id)

    def perform_create(self, serializer):
        resource_id = self.kwargs['resource_id']
        resource = Resource.objects.get(id=resource_id)
        serializer.save(user=self.request.user, resource=resource)
        
class CreateCheckoutSessionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, resource_id):
        try:
            resource = Resource.objects.get(id=resource_id)
        except Resource.DoesNotExist:
            return Response({'error': 'Resource not found.'}, status=status.HTTP_404_NOT_FOUND)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': resource.name,
                    },
                    'unit_amount': 2000,  # Example amount in cents ($20.00)
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f"{settings.SITE_URL}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{settings.SITE_URL}/cancel/",
            metadata={
                'user_id': request.user.id,
                'resource_id': resource.id,
            },
        )
        return Response({'checkout_url': checkout_session.url}, status=status.HTTP_200_OK)
    
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session['metadata']['user_id']
        resource_id = session['metadata']['resource_id']
        user = User.objects.get(id=user_id)
        resource = Resource.objects.get(id=resource_id)
        
        # Example: Create a booking after successful payment
        Booking.objects.create(
            user=user,
            resource=resource,
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=2)
        )

    return HttpResponse(status=200)
