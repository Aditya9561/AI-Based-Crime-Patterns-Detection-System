import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create or update the deployment superuser."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not all([username, email, password]):
            raise CommandError("Admin environment variables are missing.")

        User = get_user_model()
        user = User.objects.filter(username=username).first()

        if user:
            if not user.is_superuser:
                raise CommandError("This username belongs to a non-superuser.")
            user.email = email
            user.is_active = True
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS("Admin password updated successfully."))
        else:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS("Deployment admin created successfully."))
