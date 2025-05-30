from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile


class ProfileAdmin(UserAdmin):
    readonly_fields = ['created_at', 'updated_at', 'last_login']
    list_display = ['username', 'email', 'type', 'is_active', 'is_staff']
    list_filter = ['type', 'is_active', 'is_staff']
    search_fields = ['username', 'email']
    ordering = ['-created_at']

    personal_info_fields = (
        'first_name', 'last_name', 'email', 'file', 'location', 'tel',
        'description', 'working_hours', 'type'
    )
    permissions_fields = ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
    important_dates_fields = ('created_at', 'updated_at', 'last_login')

    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        ('Personal info', {'fields': personal_info_fields}),
        ('Permissions', {'fields': permissions_fields}),
    )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': personal_info_fields}),
        ('Permissions', {'fields': permissions_fields}),
        ('Important dates', {'fields': important_dates_fields}),
    )

admin.site.register(Profile, ProfileAdmin)