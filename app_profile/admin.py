from django.contrib import admin
from app_profile.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'username',
        'email',
        'user_type',
        'first_name',
        'last_name',
        'file',
        'location',
        'tel',
        'description',
        'working_hours',
        'created_at',
        'updated_at',
    ]

    search_fields = ['user__username', 'user__email', 'first_name', 'last_name']
    ordering = ['user__username']

    base_fields = (
        'first_name',
        'last_name',
        'file',
        'location',
        'tel',
        'description',
        'working_hours',
    )

    timestamp_fields = ('created_at', 'updated_at')
    readonly_on_edit = ('id', 'username', 'email', 'user_type') + timestamp_fields

    def get_fieldsets(self, request, obj=None):
        """Return fieldsets depending on whether creating or editing."""
        fieldsets = []

        if obj:
            fieldsets.append(('User Info', {'fields': ('id', 'username', 'email', 'user_type')}))
            fieldsets.append(('Profile Details', {'fields': self.base_fields}))
            fieldsets.append(('Timestamps', {'fields': self.timestamp_fields}))
        else:
            fieldsets.append(('User Info', {'fields': ('user',)}))
            fieldsets.append(('Profile Details', {'fields': self.base_fields}))

        return tuple(fieldsets)

    def get_readonly_fields(self, request, obj=None):
        """Make certain fields readonly when editing."""
        return self.readonly_on_edit if obj else ()

    def username(self, obj):
        return obj.user.username
    username.short_description = "Username"

    def email(self, obj):
        return obj.user.email
    email.short_description = "Email"

    def user_type(self, obj):
        return obj.user.type
    user_type.short_description = "Type"
