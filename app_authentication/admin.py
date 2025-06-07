from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app_authentication.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    readonly_fields = ['created_at', 'updated_at', 'last_login']
    list_display = ['id', 'username', 'email', 'type', 'is_active', 'is_staff', 'is_guest']
    list_filter = ['type', 'is_active', 'is_staff', 'is_guest']
    search_fields = ['username', 'email']
    ordering = ['username', 'created_at']

    personal_info_fields = ('email', 'type', 'is_guest')
    permissions_fields = ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
    important_dates_fields = ('created_at', 'updated_at', 'last_login')

    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('username', 'password1', 'password2')}),
        ('Personal info', {'classes': ('wide',), 'fields': personal_info_fields}),
        ('Permissions', {'classes': ('wide',), 'fields': permissions_fields}),
    )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': personal_info_fields}),
        ('Permissions', {'fields': permissions_fields}),
        ('Important dates', {'fields': important_dates_fields}),
    )