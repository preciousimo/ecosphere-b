from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class SmartHomeDevice(models.Model):
    DEVICE_TYPE_CHOICES = [
        ('thermostat', 'Thermostat'),
        ('light', 'Smart Light'),
        ('plug', 'Smart Plug'),
        ('camera', 'Security Camera'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='smart_devices')
    device_name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=50, choices=DEVICE_TYPE_CHOICES)
    device_identifier = models.CharField(max_length=100, unique=True)  # e.g., MAC address or UUID
    is_active = models.BooleanField(default=True)
    last_sync = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.device_name} ({self.device_type})"

class EnergyUsage(models.Model):
    device = models.ForeignKey(SmartHomeDevice, on_delete=models.CASCADE, related_name='energy_usages')
    timestamp = models.DateTimeField(default=timezone.now)
    energy_consumed = models.FloatField(help_text="Energy consumed in kilowatt-hours (kWh)")

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.device.device_name} - {self.energy_consumed} kWh at {self.timestamp}"

class EnergySavingRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='energy_recommendations')
    recommendation_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Recommendation for {self.user.username} at {self.created_at}"

class CommunityEnergyGoal(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    target_energy_reduction = models.FloatField(help_text="Target reduction in kWh")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    current_progress = models.FloatField(default=0.0, help_text="Current energy reduction in kWh")

    def __str__(self):
        return self.title

    def update_progress(self, energy_reduced):
        self.current_progress += energy_reduced
        self.save()

class UserCommunityProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='community_progress')
    community_goal = models.ForeignKey(CommunityEnergyGoal, on_delete=models.CASCADE, related_name='user_progress')
    energy_contributed = models.FloatField(default=0.0, help_text="Energy reduced in kWh")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'community_goal')

    def __str__(self):
        return f"{self.user.username} - {self.community_goal.title} - {self.energy_contributed} kWh"