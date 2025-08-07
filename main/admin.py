from django.contrib import admin
from .models import CV


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
