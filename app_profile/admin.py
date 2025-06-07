from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileCustomerAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at']
    list_display = ['first_name', 'last_name']
    ordering = ['user__username', 'created_at']

    fieldsets = (
        ('User info', {
            'fields': ('user',)
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours')
        }),
        ('Important dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )