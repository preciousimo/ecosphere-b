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