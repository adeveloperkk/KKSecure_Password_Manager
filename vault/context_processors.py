from vault.models import RegistrationControl

def registration_enabled(request):
    reg_control = RegistrationControl.objects.first()
    return {'registration_enabled': reg_control.enabled if reg_control else True}
