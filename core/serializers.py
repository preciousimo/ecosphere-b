from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    SustainabilityPreferences, Resource, Booking, Review,
    WasteEntry, RecyclingCenter, EcoChallenge, UserChallenge, Leaderboard
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
    
class ResourceSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    average_rating = serializers.FloatField(source='get_average_rating', read_only=True)

    class Meta:
        model = Resource
        fields = ['id', 'name', 'description', 'category', 'available', 'owner', 'created_at', 'average_rating']

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    resource = serializers.ReadOnlyField(source='resource.id')

    class Meta:
        model = Booking
        fields = ['id', 'resource', 'user', 'start_time', 'end_time', 'created_at']

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("End time must be after start time.")
        return data

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    resource = serializers.ReadOnlyField(source='resource.id')

    class Meta:
        model = Review
        fields = ['id', 'resource', 'user', 'rating', 'comment', 'created_at']

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
    
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