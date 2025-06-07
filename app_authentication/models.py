from django.db import models
from django.core.exceptions import ValidationError
from app_abstract_user.models import AbstractUser


class UserType(models.TextChoices):
    CUSTOMER = 'CUSTOMER', 'Customer'
    BUSINESS = 'BUSINESS', 'Business'
    SUPERUSER = 'SUPERUSER', 'Superuser'


class User(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    type = models.CharField(choices=UserType.choices, max_length=16)
    is_guest = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['type']

    def clean(self):
        super().clean()

        if self.is_guest and self.email:
            raise ValidationError('Guest users must not have an email address.')

        if self.is_guest and (self.is_superuser or self.is_staff or self.type == UserType.SUPERUSER):
            raise ValidationError("A guest user cannot be a superuser, staff member, or have the type 'SUPERUSER'.")

        if self.is_superuser and self.type != UserType.SUPERUSER:
            raise ValidationError('Superusers must have the user type SUPERUSER.')

        if self.is_superuser:
            return

        if not self.is_guest and not self.email:
            raise ValidationError({'email': 'Email is required'})

        if not self.is_superuser and not self.type:
            raise ValidationError({'type': 'Type is required'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)