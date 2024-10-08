from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User

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

