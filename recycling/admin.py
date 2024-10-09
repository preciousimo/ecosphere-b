from django.contrib import admin
from .models import (
    WasteEntry, RecyclingCenter,
    EcoChallenge, UserChallenge, Leaderboard
)

admin.site.register(WasteEntry)
admin.site.register(RecyclingCenter)
admin.site.register(EcoChallenge)
admin.site.register(UserChallenge)
admin.site.register(Leaderboard)
