from users.models import CustomUser
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates a superuser.'

    def handle(self, *args, **options):
        if not CustomUser.objects.filter(username='admin123').exists():
            CustomUser.objects.create_superuser(
                email="admin123@admin.com",
                username='admin123',
                password='password7791'
            )
        print('Superuser has been created.')