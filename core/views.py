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
    SmartHomeDevice,
    EnergyUsage, EnergySavingRecommendation, CommunityEnergyGoal,
    UserCommunityProgress, CommunityGarden, SeasonalPlantingGuide,
    ProduceExchangeListing, GardeningTip
)
from .serializers import (
    UserProfileSerializer, SmartHomeDeviceSerializer,
    EnergyUsageSerializer, EnergySavingRecommendationSerializer,
    CommunityEnergyGoalSerializer, UserCommunityProgressSerializer,
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
    
# SmartHomeDevice Views
class SmartHomeDeviceListCreateView(generics.ListCreateAPIView):
    queryset = SmartHomeDevice.objects.all()
    serializer_class = SmartHomeDeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name__in=['Admin', 'Moderator']).exists():
            return SmartHomeDevice.objects.all()
        return SmartHomeDevice.objects.filter(user=user)

class SmartHomeDeviceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SmartHomeDevice.objects.all()
    serializer_class = SmartHomeDeviceSerializer
    permission_classes = [IsOwnerOrReadOnly]

# EnergyUsage Views
class EnergyUsageListCreateView(generics.ListCreateAPIView):
    queryset = EnergyUsage.objects.all()
    serializer_class = EnergyUsageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        device_id = self.request.data.get('device_id')
        try:
            device = SmartHomeDevice.objects.get(id=device_id, user=self.request.user)
        except SmartHomeDevice.DoesNotExist:
            return Response({'error': 'Smart Home Device not found or not owned by the user.'}, status=status.HTTP_404_NOT_FOUND)
        serializer.save(device=device)

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name__in=['Admin', 'Moderator']).exists():
            return EnergyUsage.objects.all()
        return EnergyUsage.objects.filter(device__user=user)

# EnergySavingRecommendation Views
class EnergySavingRecommendationListView(generics.ListAPIView):
    serializer_class = EnergySavingRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EnergySavingRecommendation.objects.filter(user=self.request.user)

class EnergySavingRecommendationMarkReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, recommendation_id):
        try:
            recommendation = EnergySavingRecommendation.objects.get(id=recommendation_id, user=request.user)
        except EnergySavingRecommendation.DoesNotExist:
            return Response({'error': 'Recommendation not found.'}, status=status.HTTP_404_NOT_FOUND)

        recommendation.is_read = True
        recommendation.save()
        return Response({'message': 'Recommendation marked as read.'}, status=status.HTTP_200_OK)

# CommunityEnergyGoal Views
class CommunityEnergyGoalListCreateView(generics.ListCreateAPIView):
    queryset = CommunityEnergyGoal.objects.all()
    serializer_class = CommunityEnergyGoalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrModerator]

    def perform_create(self, serializer):
        serializer.save()

class CommunityEnergyGoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CommunityEnergyGoal.objects.all()
    serializer_class = CommunityEnergyGoalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrModerator]

# UserCommunityProgress Views
class UserCommunityProgressListView(generics.ListAPIView):
    serializer_class = UserCommunityProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserCommunityProgress.objects.filter(user=self.request.user)

class UserCommunityProgressUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, community_goal_id):
        try:
            community_goal = CommunityEnergyGoal.objects.get(id=community_goal_id)
        except CommunityEnergyGoal.DoesNotExist:
            return Response({'error': 'Community Energy Goal not found.'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        energy_reduced = request.data.get('energy_reduced')

        if not energy_reduced:
            return Response({'error': 'Please provide energy_reduced value.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            energy_reduced = float(energy_reduced)
            if energy_reduced <= 0:
                raise ValueError
        except ValueError:
            return Response({'error': 'energy_reduced must be a positive number.'}, status=status.HTTP_400_BAD_REQUEST)

        # Update or create UserCommunityProgress
        user_progress, created = UserCommunityProgress.objects.get_or_create(user=user, community_goal=community_goal)
        user_progress.energy_contributed += energy_reduced
        user_progress.save()

        # Update CommunityEnergyGoal progress
        community_goal.update_progress(energy_reduced)

        # Optionally, create EnergySavingRecommendation based on progress
        if community_goal.current_progress >= (0.75 * community_goal.target_energy_reduction):
            EnergySavingRecommendation.objects.create(
                user=user,
                recommendation_text="Great job! You're helping the community reach 75% of our energy reduction goal. Keep it up!"
            )

        return Response({'message': 'Energy contribution updated successfully.'}, status=status.HTTP_200_OK)

# Personalized Energy-Saving Recommendations
class GenerateEnergySavingRecommendationsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        # Example logic: Analyze user's energy usage and generate recommendations
        # This can be enhanced with AI/ML models for better recommendations

        total_energy = EnergyUsage.objects.filter(device__user=user).aggregate(Sum('energy_consumed'))['energy_consumed__sum'] or 0

        recommendations = []
        if total_energy > 100:
            recommendations.append("Consider using energy-efficient appliances to reduce your consumption.")
        if any(device.device_type == 'thermostat' for device in user.smart_devices.all()):
            recommendations.append("Optimize your thermostat settings to save energy during peak hours.")
        else:
            recommendations.append("Consider installing a smart thermostat for better energy management.")

        for rec in recommendations:
            EnergySavingRecommendation.objects.create(
                user=user,
                recommendation_text=rec
            )

        serialized_recs = EnergySavingRecommendationSerializer(EnergySavingRecommendation.objects.filter(user=user, is_read=False), many=True)
        return Response(serialized_recs.data, status=status.HTTP_200_OK)
    
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