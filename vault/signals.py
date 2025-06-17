from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import SystemLog

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    SystemLog.objects.create(
        admin_user=user,
        action='login',
        object_type='User',
        object_id=str(user.id),
        session_key=request.session.session_key,
        details='User logged in.'
    )

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    if user is not None:
        SystemLog.objects.create(
            admin_user=user,
            action='logout',
            object_type='User',
            object_id=str(user.id),
            session_key=request.session.session_key,
            details='User logged out.'
        )