from django.db import models
from app_user.models import User


class Profile(models.Model):
    class ProfileType(models.TextChoices):
        CUSTOMER = 'CUSTOMER', 'Customer',
        BUSINESS = 'BUSINESS', 'Business'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_type = models.CharField(max_length=8, choices=ProfileType.choices)

    def __str__(self):
        return f"{self.user.email} {self.profile_type}"