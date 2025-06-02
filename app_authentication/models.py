from django.db import models
from django.core.exceptions import ValidationError
from app_user.models import User
from core.models import TimeStamped


class AccountType(models.TextChoices):
    CUSTOMER = 'CUSTOMER', 'Customer'
    BUSINESS = 'BUSINESS', 'Business'
    SUPERUSER = 'SUPERUSER', 'Superuser'


class Account(User, TimeStamped):
    email = models.EmailField(unique=True, null=True, blank=True)
    type = models.CharField(choices=AccountType.choices, max_length=16)
    is_guest = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['type']

    def clean(self):
        super().clean()

        if self.is_guest and self.email:
            raise ValidationError('Guest users must not have an email address.')

        if self.is_guest and (self.is_superuser or self.is_staff or self.type == AccountType.SUPERUSER):
            raise ValidationError("A guest account cannot be a superuser, staff member, or have the type 'SUPERUSER'.")

        if self.is_superuser and self.type != AccountType.SUPERUSER:
            raise ValidationError('Superusers must have the account type SUPERUSER.')

        if self.is_superuser:
            return

        if not self.is_guest and not self.email:
            raise ValidationError({'email': 'Email is required'})

        if not self.is_superuser and not self.type:
            raise ValidationError({'type': 'Type is required'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)