from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class Resource(models.Model):
    CATEGORY_CHOICES = [
        ('tool', 'Tool'),
        ('vehicle', 'Vehicle'),
        ('equipment', 'Equipment'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_resources')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return reviews.aggregate(models.Avg('rating'))['rating__avg']
        return 0

class Booking(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.resource.name} booked by {self.user.username} from {self.start_time} to {self.end_time}"

    class Meta:
        unique_together = ('resource', 'start_time', 'end_time')

class Review(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()  # e.g., 1 to 5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review of {self.resource.name} by {self.user.username}"


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    
class WasteEntry(models.Model):
    WASTE_TYPE_CHOICES = [
        ('plastic', 'Plastic'),
        ('paper', 'Paper'),
        ('glass', 'Glass'),
        ('metal', 'Metal'),
        ('organic', 'Organic'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='waste_entries')
    waste_type = models.CharField(max_length=50, choices=WASTE_TYPE_CHOICES)
    quantity = models.FloatField(help_text="Quantity in kilograms")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.waste_type} - {self.quantity}kg"

class RecyclingCenter(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

class EcoChallenge(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    points = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.title

class UserChallenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_challenges')
    challenge = models.ForeignKey(EcoChallenge, on_delete=models.CASCADE, related_name='user_challenges')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title}"

class Leaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='leaderboard')
    points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.points} Points"

    def update_points(self, additional_points):
        self.points += additional_points
        self.save()
        
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
    
class CommunityGarden(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gardens')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SeasonalPlantingGuide(models.Model):
    SEASON_CHOICES = [
        ('spring', 'Spring'),
        ('summer', 'Summer'),
        ('autumn', 'Autumn'),
        ('winter', 'Winter'),
    ]

    season = models.CharField(max_length=20, choices=SEASON_CHOICES)
    plant_name = models.CharField(max_length=100)
    planting_start = models.DateField()
    planting_end = models.DateField()
    harvest_start = models.DateField()
    harvest_end = models.DateField()
    tips = models.TextField()

    def __str__(self):
        return f"{self.plant_name} - {self.get_season_display()}"

class ProduceExchangeListing(models.Model):
    PRODUCE_TYPE_CHOICES = [
        ('vegetable', 'Vegetable'),
        ('fruit', 'Fruit'),
        ('herb', 'Herb'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='produce_listings')
    garden = models.ForeignKey(CommunityGarden, on_delete=models.CASCADE, related_name='produce_listings')
    produce_type = models.CharField(max_length=50, choices=PRODUCE_TYPE_CHOICES)
    produce_name = models.CharField(max_length=100)
    quantity_available = models.PositiveIntegerField(help_text="Quantity available (units)")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.produce_name} by {self.user.username} at {self.garden.name}"

class GardeningTip(models.Model):
    CATEGORY_CHOICES = [
        ('planting', 'Planting'),
        ('maintenance', 'Maintenance'),
        ('pest_control', 'Pest Control'),
        ('harvesting', 'Harvesting'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='gardening_tips')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

def create_custom_permissions():
    content_type = ContentType.objects.get_for_model(Resource)
    Permission.objects.get_or_create(
        codename='can_approve_resources',
        name='Can approve resources',
        content_type=content_type,
    )
    
    content_type = ContentType.objects.get_for_model(Event)
    Permission.objects.get_or_create(
        codename='can_feature_events',
        name='Can feature events',
        content_type=content_type,
    )

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
    moderator_permissions = Permission.objects.filter(
        codename__in=['add_user', 'change_user', 'view_user', 'can_approve_resources', 'can_feature_events']
    )
    moderator_group.permissions.set(moderator_permissions)

# Run these functions when the app is ready
from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        create_groups()
        create_custom_permissions()
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