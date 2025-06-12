from django.contrib import admin
from .models import PasswordEntry

@admin.register(PasswordEntry)
class PasswordEntryAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'site_url', 'username', 'notes', 'created_at', 'updated_at', 'user')
    search_fields = ('site_name', 'site_url', 'username', 'notes', 'user__username')
    list_filter = ('site_name', 'user', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at', 'user')
    exclude = ('password_encrypted',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)
