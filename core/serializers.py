from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    SustainabilityPreferences,
    WasteEntry, RecyclingCenter, EcoChallenge, UserChallenge,
    Leaderboard, SmartHomeDevice, EnergyUsage, EnergySavingRecommendation,
    CommunityEnergyGoal, UserCommunityProgress,
    CommunityGarden, SeasonalPlantingGuide, ProduceExchangeListing, GardeningTip
)

class SustainabilityPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SustainabilityPreferences
        fields = ['interests', 'carbon_footprint_goal', 'preferred_community_radius']

class UserProfileSerializer(serializers.ModelSerializer):
    sustainability_preferences = SustainabilityPreferencesSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'sustainability_preferences']
        read_only_fields = ['id', 'username', 'email']

    def update(self, instance, validated_data):
        preferences_data = validated_data.pop('sustainability_preferences', {})
        preferences = instance.sustainability_preferences

        for attr, value in preferences_data.items():
            setattr(preferences, attr, value)
        preferences.save()

        return instance
    
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
        
class CommunityGardenSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = CommunityGarden
        fields = ['id', 'name', 'description', 'address', 'latitude', 'longitude', 'contact_email', 'contact_phone', 'owner', 'created_at']
        read_only_fields = ['id', 'owner', 'created_at']

class SeasonalPlantingGuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeasonalPlantingGuide
        fields = ['id', 'season', 'plant_name', 'planting_start', 'planting_end', 'harvest_start', 'harvest_end', 'tips']
        read_only_fields = ['id']

class ProduceExchangeListingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    garden = serializers.ReadOnlyField(source='garden.name')

    class Meta:
        model = ProduceExchangeListing
        fields = ['id', 'user', 'garden', 'produce_type', 'produce_name', 'quantity_available', 'description', 'created_at']
        read_only_fields = ['id', 'user', 'garden', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        garden_id = self.context['request'].data.get('garden_id')
        try:
            garden = CommunityGarden.objects.get(id=garden_id, owner=user)
        except CommunityGarden.DoesNotExist:
            raise serializers.ValidationError("Community Garden not found or you do not have permission to add listings to this garden.")
        return ProduceExchangeListing.objects.create(user=user, garden=garden, **validated_data)

class GardeningTipSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = GardeningTip
        fields = ['id', 'title', 'category', 'content', 'author', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']
