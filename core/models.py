from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class SustainabilityPreferences(models.Model):
    INTEREST_CHOICES = [
        ('energy', 'Renewable Energy'),
        ('waste', 'Waste Reduction'),
        ('transport', 'Sustainable Transportation'),
        ('food', 'Sustainable Food'),
        ('water', 'Water Conservation'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='sustainability_preferences')
    interests = models.JSONField(default=list)
    carbon_footprint_goal = models.FloatField(null=True, blank=True)
    preferred_community_radius = models.IntegerField(default=10)  # in kilometers

    def __str__(self):
        return f"{self.user.username}'s Sustainability Preferences"

@receiver(post_save, sender=User)
def create_user_preferences(sender, instance, created, **kwargs):
    if created:
        SustainabilityPreferences.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_preferences(sender, instance, **kwargs):
    instance.sustainability_preferences.save()