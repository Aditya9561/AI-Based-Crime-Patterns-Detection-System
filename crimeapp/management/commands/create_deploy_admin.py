import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create a superuser from deployment environment variables."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not all([username, email, password]):
            raise CommandError("Admin environment variables are missing.")

        User = get_user_model()

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.is_superuser:
                self.stdout.write(self.style.SUCCESS("Admin account already exists."))
                return
            raise CommandError("Username already exists but is not a superuser. Choose another username.")

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        self.stdout.write(self.style.SUCCESS("Deployment admin created successfully."))
