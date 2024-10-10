from django.contrib import admin
from .models import (
    SustainabilityPreferences, CommunityGarden,
    SeasonalPlantingGuide, ProduceExchangeListing, GardeningTip
)

admin.site.register(SustainabilityPreferences)
admin.site.register(CommunityGarden)
admin.site.register(SeasonalPlantingGuide)
admin.site.register(ProduceExchangeListing)
admin.site.register(GardeningTip)
