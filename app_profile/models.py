from django.db import models
from app_authentication.models import User, UserType
from django.db.models import Q


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to=~Q(type=UserType.SUPERUSER),
        related_name='profile'
    )
    first_name = models.CharField(max_length=32, blank=True, default='')
    last_name = models.CharField(max_length=32, blank=True, default='')
    file = models.FileField(null=True, blank=True)
    location = models.CharField(max_length=64, blank=True, default='')
    tel = models.CharField(max_length=32, blank=True, default='')
    description = models.TextField(blank=True, default='')
    working_hours = models.CharField(max_length=64, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}"

