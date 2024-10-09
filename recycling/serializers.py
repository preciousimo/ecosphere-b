from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    WasteEntry, RecyclingCenter, EcoChallenge, UserChallenge,
    Leaderboard
)
    
class WasteEntrySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = WasteEntry
        fields = ['id', 'user', 'waste_type', 'quantity', 'date']
        read_only_fields = ['id', 'user', 'date']

class RecyclingCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecyclingCenter
        fields = ['id', 'name', 'address', 'latitude', 'longitude', 'contact_email', 'contact_phone']
        read_only_fields = ['id']

class EcoChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcoChallenge
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'points']
        read_only_fields = ['id']

class UserChallengeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    challenge = serializers.ReadOnlyField(source='challenge.title')

    class Meta:
        model = UserChallenge
        fields = ['id', 'user', 'challenge', 'completed', 'completed_at']
        read_only_fields = ['id', 'user', 'challenge', 'completed_at']

class LeaderboardSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Leaderboard
        fields = ['user', 'points']
        read_only_fields = ['user', 'points']
