from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone
from django.db.models import Sum
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from recycling.models import (
    WasteEntry, RecyclingCenter,
    EcoChallenge, UserChallenge, Leaderboard
)
from recycling.serializers import (
    WasteEntrySerializer, RecyclingCenterSerializer, EcoChallengeSerializer,
    UserChallengeSerializer, LeaderboardSerializer
)
from core.permissions import (
    IsAdminOrModerator, IsOwnerOrReadOnly, IsAdminUser, IsAuthorOrReadOnly
)
import logging

logger = logging.getLogger(__name__)

# WasteEntry Views
class WasteEntryListCreateView(generics.ListCreateAPIView):
    queryset = WasteEntry.objects.all()
    serializer_class = WasteEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Users can see their own waste entries; Admins can see all
        user = self.request.user
        if user.groups.filter(name__in=['Admin', 'Moderator']).exists():
            return WasteEntry.objects.all()
        return WasteEntry.objects.filter(user=user)

# RecyclingCenter Views
class RecyclingCenterListCreateView(generics.ListCreateAPIView):
    queryset = RecyclingCenter.objects.all()
    serializer_class = RecyclingCenterSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrModerator]

    def perform_create(self, serializer):
        serializer.save()

class RecyclingCenterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecyclingCenter.objects.all()
    serializer_class = RecyclingCenterSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrModerator]

# EcoChallenge Views
class EcoChallengeListCreateView(generics.ListCreateAPIView):
    queryset = EcoChallenge.objects.all()
    serializer_class = EcoChallengeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrModerator]

    def perform_create(self, serializer):
        serializer.save()

class EcoChallengeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EcoChallenge.objects.all()
    serializer_class = EcoChallengeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrModerator]

# UserChallenge Views
class UserChallengeListView(generics.ListAPIView):
    serializer_class = UserChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserChallenge.objects.filter(user=self.request.user)

class UserChallengeCompleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, challenge_id):
        try:
            challenge = EcoChallenge.objects.get(id=challenge_id)
        except EcoChallenge.DoesNotExist:
            return Response({'error': 'Challenge not found.'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        # Check if challenge is active
        now = timezone.now()
        if not (challenge.start_date <= now <= challenge.end_date):
            return Response({'error': 'Challenge is not active.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user already completed the challenge
        user_challenge, created = UserChallenge.objects.get_or_create(user=user, challenge=challenge)
        if user_challenge.completed:
            return Response({'message': 'Challenge already completed.'}, status=status.HTTP_200_OK)

        # Mark as completed
        user_challenge.completed = True
        user_challenge.completed_at = timezone.now()
        user_challenge.save()

        # Update leaderboard
        leaderboard, _ = Leaderboard.objects.get_or_create(user=user)
        leaderboard.update_points(challenge.points)

        return Response({'message': 'Challenge completed successfully!', 'points_awarded': challenge.points}, status=status.HTTP_200_OK)

# Leaderboard Views
class LeaderboardListView(generics.ListAPIView):
    serializer_class = LeaderboardSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Leaderboard.objects.all().order_by('-points')[:10]  # Top 10 users

# Additional Views for Aggregated Data (Optional)
class UserWasteSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        waste_summary = WasteEntry.objects.filter(user=user).values('waste_type').annotate(total_quantity=Sum('quantity'))
        return Response(waste_summary, status=status.HTTP_200_OK)
