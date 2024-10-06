from rest_framework import serializers
from django.contrib.auth.models import User
from .models import SustainabilityPreferences

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