from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class ProfileManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set.')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(username, password, **extra_fields)


class ProfileType(models.TextChoices):
    CUSTOMER = 'CUSTOMER', 'Customer'
    FREELANCER = 'FREELANCER', 'Freelancer'


class Profile(AbstractBaseUser, PermissionsMixin):
    username = models.CharField (max_length=32, unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=32, blank=True, default='')
    last_name = models.CharField(max_length=32, blank=True, default='')
    file = models.FileField(null=True, blank=True)
    location = models.CharField(max_length=64, blank=True, default='')
    tel = models.CharField(max_length=32, blank=True, default='')
    description = models.TextField(blank=True, default='')
    working_hours = models.CharField(max_length=64, blank=True, default='')
    type = models.CharField(max_length=16, choices=ProfileType.choices)
    email = models.EmailField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_guest = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'type']

    def clean(self):
        super().clean()
        if not self.is_guest and not self.email:
            raise ValidationError({'email': 'Email is required'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username}"