from django.contrib import admin
from .models import Profile
from django.contrib.auth.hashers import make_password


class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'last_login']



admin.site.register(Profile, ProfileAdmin)