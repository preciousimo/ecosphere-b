from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    SustainabilityPreferences, CommunityGarden, 
    SeasonalPlantingGuide, ProduceExchangeListing, GardeningTip
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
