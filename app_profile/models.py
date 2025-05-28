from django.core.exceptions import ValidationError
from django.db import models
from app_user.models import User


class Profile(models.Model):
    class ProfileType(models.TextChoices):
        CUSTOMER = 'CUSTOMER', 'Customer',
        FREELANCER = 'FREELANCER', 'Freelancer'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(unique = True, null=True, blank=True)
    is_guest = models.BooleanField(default=False)
    profile_type = models.CharField(max_length=16, choices=ProfileType.choices)

    def clean(self):
        super().clean()
        if not self.is_guest and not self.email:
            raise ValidationError({'email': 'Email is required'})

    def __str__(self):
        return f"{self.user.username} {self.email} {self.profile_type}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)