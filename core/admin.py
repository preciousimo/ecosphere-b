from django.contrib import admin
from .models import (
    Resource, Booking, Review, WasteEntry, RecyclingCenter,
    EcoChallenge, UserChallenge, Leaderboard, SustainabilityPreferences,
    SmartHomeDevice, EnergyUsage, EnergySavingRecommendation,
    CommunityEnergyGoal, UserCommunityProgress
)

admin.site.register(Resource)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(WasteEntry)
admin.site.register(RecyclingCenter)
admin.site.register(EcoChallenge)
admin.site.register(UserChallenge)
admin.site.register(Leaderboard)
admin.site.register(SustainabilityPreferences)
admin.site.register(SmartHomeDevice)
admin.site.register(EnergyUsage)
admin.site.register(EnergySavingRecommendation)
admin.site.register(CommunityEnergyGoal)
admin.site.register(UserCommunityProgress)
