from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Resource, Booking, Review,
)
    
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
