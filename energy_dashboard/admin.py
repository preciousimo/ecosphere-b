from django.contrib import admin
from energy_dashboard.models import (
    SmartHomeDevice, EnergyUsage, EnergySavingRecommendation,
    CommunityEnergyGoal, UserCommunityProgress
)

admin.site.register(SmartHomeDevice)
admin.site.register(EnergyUsage)
admin.site.register(EnergySavingRecommendation)
admin.site.register(CommunityEnergyGoal)
admin.site.register(UserCommunityProgress)
