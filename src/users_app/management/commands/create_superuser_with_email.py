from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create a superuser with username and email.'

    def add_arguments(self, parser):
        parser.add_argument('--username', dest='username', type=str)
        parser.add_argument('--email', dest='email', type=str)
        parser.add_argument('--password', dest='password', type=str)

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        if not all([username, email, password]):
            self.stdout.write(self.style.ERROR('Please provide username, email, and password.'))
            return

        User = get_user_model()
        user = User.objects.create_superuser(username, email, password)
        self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" (email: {email}) created successfully.'))
