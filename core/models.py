from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission

# Create default groups
def create_groups():
    groups = ['Admin', 'Moderator', 'Regular User']
    for group_name in groups:
        Group.objects.get_or_create(name=group_name)

# Assign permissions to groups
def assign_permissions():
    admin_group = Group.objects.get(name='Admin')
    moderator_group = Group.objects.get(name='Moderator')
    
    # Assign all permissions to Admin group
    admin_group.permissions.set(Permission.objects.all())
    
    # Assign specific permissions to Moderator group
    moderator_permissions = Permission.objects.filter(codename__in=['add_user', 'change_user', 'view_user'])
    moderator_group.permissions.set(moderator_permissions)

# Run these functions when the app is ready
from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        create_groups()
        assign_permissions()

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