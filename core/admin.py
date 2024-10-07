from django.contrib import admin
from .models import (
    Resource, Booking, Review, WasteEntry, RecyclingCenter,
    EcoChallenge, UserChallenge, Leaderboard, SustainabilityPreferences
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
