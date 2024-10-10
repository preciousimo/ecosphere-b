from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.conf import settings
from django.db.models import Sum
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from energy_dashboard.models import (
    SmartHomeDevice,
    EnergyUsage, EnergySavingRecommendation, CommunityEnergyGoal,
    UserCommunityProgress
)
from energy_dashboard.serializers import (
    SmartHomeDeviceSerializer,
    EnergyUsageSerializer, EnergySavingRecommendationSerializer,
    CommunityEnergyGoalSerializer, UserCommunityProgressSerializer,
)
from core.permissions import (
    IsAdminOrModerator, IsOwnerOrReadOnly, IsAdminUser, IsAuthorOrReadOnly
)
import logging

logger = logging.getLogger(__name__)
    
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
