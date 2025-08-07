from django.contrib import admin
from .models import CV, RequestLog


@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    """Admin configuration for CV model."""
    list_display = ('firstname', 'lastname', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('firstname', 'lastname', 'skills', 'bio')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Personal Information', {
            'fields': ('firstname', 'lastname')
        }),
        ('Professional Information', {
            'fields': ('bio', 'skills', 'projects')
        }),
        ('Contact Information', {
            'fields': ('contacts',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    """Admin configuration for RequestLog model."""
    list_display = ('method', 'path', 'response_status', 'response_time', 'timestamp', 'remote_ip', 'is_authenticated')
    list_filter = ('method', 'response_status', 'is_authenticated', 'timestamp')
    search_fields = ('path', 'remote_ip', 'user_agent')
    readonly_fields = ('timestamp', 'method', 'path', 'query_string', 'remote_ip', 'user_agent', 'response_status', 'response_time', 'user', 'is_authenticated')
    ordering = ('-timestamp',)
    
    fieldsets = (
        ('Request Information', {
            'fields': ('method', 'path', 'query_string', 'remote_ip', 'user_agent')
        }),
        ('Response Information', {
            'fields': ('response_status', 'response_time')
        }),
        ('User Information', {
            'fields': ('user', 'is_authenticated')
        }),
        ('Timestamp', {
            'fields': ('timestamp',)
        }),
    )
    
    def has_add_permission(self, request):
        """Disable adding RequestLog entries manually."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Disable editing RequestLog entries."""
        return False
