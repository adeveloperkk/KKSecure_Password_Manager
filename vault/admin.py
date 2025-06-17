from django.contrib import admin
from django.contrib.sessions.models import Session
from django.utils.html import format_html
from django.contrib.auth.models import User
from .models import PasswordEntry, WalletEntry, Note, SaveEvent, SystemLog, RegistrationControl
from django.urls import path
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.admin.sites import NotRegistered

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

@admin.register(WalletEntry)
class WalletEntryAdmin(admin.ModelAdmin):
    list_display = ('wallet_type', 'user', 'card_number', 'bank_name', 'account_number', 'created_at', 'updated_at')
    search_fields = ('card_number', 'bank_name', 'account_number', 'user__username')
    list_filter = ('wallet_type', 'user', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at', 'user')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'updated_at')
    search_fields = ('title', 'content', 'user__username')
    list_filter = ('user', 'updated_at')
    readonly_fields = ('created_at', 'updated_at', 'user')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)

@admin.register(SaveEvent)
class SaveEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'event_date', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'user__username')
    list_filter = ('user', 'event_date', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at', 'user')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)

class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'user', 'ip', 'expire_date', 'session_actions')
    readonly_fields = ('session_key', 'expire_date')
    actions = ['terminate_selected_sessions']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('terminate-session/<str:session_key>/', self.admin_site.admin_view(self.terminate_session_view), name='terminate-session'),
        ]
        return custom_urls + urls

    def terminate_session_view(self, request, session_key):
        from django.contrib.sessions.models import Session
        from django.contrib.auth import logout
        try:
            session = Session.objects.get(session_key=session_key)
            session.delete()
            if session_key == request.session.session_key:
                logout(request)
                return HttpResponseRedirect(reverse('admin:login') + '?next=/admin/')
            self.message_user(request, f"Session {session_key} terminated.")
        except Session.DoesNotExist:
            self.message_user(request, f"Session {session_key} does not exist.", level='error')
        return HttpResponseRedirect(reverse('admin:sessions_session_changelist'))

    def user(self, obj):
        data = obj.get_decoded()
        uid = data.get('_auth_user_id')
        if uid:
            try:
                return User.objects.get(pk=uid)
            except User.DoesNotExist:
                return '-'
        return '-'

    def ip(self, obj):
        data = obj.get_decoded()
        return data.get('ip', '-') or data.get('ip_address', '-')

    def session_actions(self, obj):
        url = reverse('admin:terminate-session', args=[obj.session_key])
        return format_html('<a class="button" href="{}">Terminate</a>', url)
    session_actions.short_description = 'Actions'

    def terminate_selected_sessions(self, request, queryset):
        current_session_key = request.session.session_key
        for session in queryset:
            # Only skip current session in bulk action
            if session.session_key != current_session_key:
                session.delete()
                SystemLog.objects.create(
                    admin_user=request.user,
                    session_key=session.session_key,
                    action='terminate',
                    details='Terminated from admin panel.'
                )
        self.message_user(request, "Selected sessions terminated (except current session).")

    terminate_selected_sessions.short_description = "Terminate selected sessions (except current)"

try:
    admin.site.unregister(Session)
except NotRegistered:
    pass
admin.site.register(Session, SessionAdmin)

@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ('admin_user', 'action', 'object_type', 'object_id', 'session_key', 'timestamp', 'details')
    search_fields = ('admin_user__username', 'action', 'object_type', 'object_id', 'session_key', 'details')
    list_filter = ('action', 'object_type', 'admin_user', 'timestamp')
    readonly_fields = ('timestamp',)

@admin.register(RegistrationControl)
class RegistrationControlAdmin(admin.ModelAdmin):
    list_display = ('enabled', 'updated_at')
    list_display_links = ('updated_at',)
    list_editable = ('enabled',)
    readonly_fields = ('updated_at',)

