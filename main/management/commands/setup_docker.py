from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
import time


class Command(BaseCommand):
    help = 'Set up the database for Docker deployment'

    def handle(self, *args, **options):
        self.stdout.write('Setting up database for Docker deployment...')
        
        # Wait for database to be ready
        self.stdout.write('Waiting for database to be ready...')
        max_attempts = 30
        attempt = 0
        
        while attempt < max_attempts:
            try:
                connection.ensure_connection()
                self.stdout.write(self.style.SUCCESS('Database connection successful!'))
                break
            except Exception as e:
                attempt += 1
                self.stdout.write(f'Database not ready yet (attempt {attempt}/{max_attempts}): {e}')
                time.sleep(2)
        else:
            self.stdout.write(self.style.ERROR('Could not connect to database after maximum attempts'))
            return
        
        # Run migrations
        self.stdout.write('Running migrations...')
        try:
            call_command('migrate')
            self.stdout.write(self.style.SUCCESS('Migrations completed successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Migration failed: {e}'))
            return
        
        # Load initial data
        self.stdout.write('Loading initial data...')
        try:
            call_command('loaddata', 'main/fixtures/sample_cv.json')
            self.stdout.write(self.style.SUCCESS('Initial data loaded successfully!'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Could not load initial data: {e}'))
        
        # Create superuser if it doesn't exist
        self.stdout.write('Creating superuser...')
        try:
            from django.contrib.auth.models import User
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser('admin', 'admin@example.com', 'adminpass123')
                self.stdout.write(self.style.SUCCESS('Superuser created successfully!'))
            else:
                self.stdout.write(self.style.SUCCESS('Superuser already exists'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Could not create superuser: {e}'))
        
        self.stdout.write(self.style.SUCCESS('Docker setup completed successfully!')) 