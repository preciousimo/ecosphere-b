from rest_framework import serializers
from django.contrib.auth.models import User
from energy_dashboard.models import (
    SmartHomeDevice, EnergyUsage, EnergySavingRecommendation,
    CommunityEnergyGoal, UserCommunityProgress
)

class SmartHomeDeviceSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = SmartHomeDevice
        fields = ['id', 'user', 'device_name', 'device_type', 'device_identifier', 'is_active', 'last_sync']
        read_only_fields = ['id', 'user', 'last_sync']

class EnergyUsageSerializer(serializers.ModelSerializer):
    device = serializers.ReadOnlyField(source='device.device_name')

    class Meta:
        model = EnergyUsage
        fields = ['id', 'device', 'timestamp', 'energy_consumed']
        read_only_fields = ['id', 'device', 'timestamp']

class EnergySavingRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergySavingRecommendation
        fields = ['id', 'user', 'recommendation_text', 'created_at', 'is_read']
        read_only_fields = ['id', 'user', 'recommendation_text', 'created_at']

class CommunityEnergyGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityEnergyGoal
        fields = ['id', 'title', 'description', 'target_energy_reduction', 'start_date', 'end_date', 'current_progress']
        read_only_fields = ['id', 'current_progress']

class UserCommunityProgressSerializer(serializers.ModelSerializer):
    community_goal = serializers.ReadOnlyField(source='community_goal.title')
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UserCommunityProgress
        fields = ['id', 'user', 'community_goal', 'energy_contributed', 'updated_at']
        read_only_fields = ['id', 'user', 'community_goal', 'updated_at']