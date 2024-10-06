from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
# from core.models import Profile  # Assuming you'll create a Profile model

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # Create a superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))

        # Create some regular users
        for i in range(1, 6):
            username = f'user{i}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username, f'{username}@example.com', 'password')
                # Assuming you have a Profile model, create a profile for each user
                # Profile.objects.create(user=user, bio=f'I am user {i}')
                self.stdout.write(self.style.SUCCESS(f'User {username} created successfully'))

        self.stdout.write(self.style.SUCCESS('Database seeded successfully'))