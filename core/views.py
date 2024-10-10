from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Sum
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    CommunityGarden, SeasonalPlantingGuide,
    ProduceExchangeListing, GardeningTip
)
from .serializers import (
    UserProfileSerializer,
    CommunityGardenSerializer, SeasonalPlantingGuideSerializer,
    ProduceExchangeListingSerializer, GardeningTipSerializer
)
from .permissions import (
    IsAdminOrModerator, IsOwnerOrReadOnly, IsAdminUser, IsAuthorOrReadOnly
)
import logging

logger = logging.getLogger(__name__)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    if request.method == 'GET':
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrModerator])
def admin_dashboard(request):
    # This view is only accessible to users in the Admin or Moderator groups
    return Response({'message': 'Welcome to the admin dashboard'})
    
# CommunityGarden Views

class CommunityGardenListCreateView(generics.ListCreateAPIView):
    queryset = CommunityGarden.objects.all()
    serializer_class = CommunityGardenSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.groups.filter(name__in=['Admin', 'Moderator']).exists():
            return CommunityGarden.objects.all()
        return CommunityGarden.objects.filter(owner=user)

class CommunityGardenDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CommunityGarden.objects.all()
    serializer_class = CommunityGardenSerializer
    permission_classes = [IsOwnerOrReadOnly | IsAdminOrModerator]

# SeasonalPlantingGuide Views

class SeasonalPlantingGuideListCreateView(generics.ListCreateAPIView):
    queryset = SeasonalPlantingGuide.objects.all()
    serializer_class = SeasonalPlantingGuideSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrModerator]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['season', 'plant_name']
    search_fields = ['plant_name', 'tips']

    def perform_create(self, serializer):
        serializer.save()

class SeasonalPlantingGuideDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SeasonalPlantingGuide.objects.all()
    serializer_class = SeasonalPlantingGuideSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrModerator]

# ProduceExchangeListing Views

class ProduceExchangeListingListCreateView(generics.ListCreateAPIView):
    queryset = ProduceExchangeListing.objects.all()
    serializer_class = ProduceExchangeListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['produce_type', 'produce_name', 'garden__name']
    search_fields = ['produce_name', 'description']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.groups.filter(name__in=['Admin', 'Moderator']).exists():
            return ProduceExchangeListing.objects.all()
        return ProduceExchangeListing.objects.filter(user=user)

class ProduceExchangeListingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProduceExchangeListing.objects.all()
    serializer_class = ProduceExchangeListingSerializer
    permission_classes = [IsOwnerOrReadOnly | IsAdminOrModerator]

# GardeningTip Views

class GardeningTipListCreateView(generics.ListCreateAPIView):
    queryset = GardeningTip.objects.all()
    serializer_class = GardeningTipSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class GardeningTipDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GardeningTip.objects.all()
    serializer_class = GardeningTipSerializer
    permission_classes = [IsAuthorOrReadOnly | IsAdminOrModerator]