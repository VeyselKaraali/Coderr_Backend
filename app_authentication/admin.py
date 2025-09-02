from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from app_authentication.models import CustomUser

admin.site.unregister(TokenProxy)
admin.site.unregister(Group)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')


@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    readonly_fields = ['is_staff', 'is_superuser', 'last_login']
    list_display = ['id', 'username', 'is_active', 'is_staff', 'is_superuser']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    search_fields = ['username']
    ordering = ['username']

    fieldsets = (
        ('Login Information', {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Activity', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        ('Create New User', {'classes': ('wide',),'fields': ('username', 'password1', 'password2')}),
    )