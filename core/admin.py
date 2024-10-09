from django.contrib import admin
from .models import (
    SustainabilityPreferences,
    SmartHomeDevice, EnergyUsage, EnergySavingRecommendation,
    CommunityEnergyGoal, UserCommunityProgress, CommunityGarden,
    SeasonalPlantingGuide, ProduceExchangeListing, GardeningTip
)

admin.site.register(SustainabilityPreferences)
admin.site.register(SmartHomeDevice)
admin.site.register(EnergyUsage)
admin.site.register(EnergySavingRecommendation)
admin.site.register(CommunityEnergyGoal)
admin.site.register(UserCommunityProgress)
admin.site.register(CommunityGarden)
admin.site.register(SeasonalPlantingGuide)
admin.site.register(ProduceExchangeListing)
admin.site.register(GardeningTip)
