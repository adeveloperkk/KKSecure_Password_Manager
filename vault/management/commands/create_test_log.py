from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from vault.models import SystemLog

class Command(BaseCommand):
    help = 'Create a test SystemLog entry.'

    def handle(self, *args, **kwargs):
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR('No users found. Please create a user first.'))
            return
        SystemLog.objects.create(
            admin_user=user,
            action='login',
            object_type='User',
            object_id=str(user.id),
            session_key='testsessionkey',
            details='Test log entry created by management command.'
        )
        self.stdout.write(self.style.SUCCESS('Test SystemLog entry created.'))
