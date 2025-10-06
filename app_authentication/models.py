from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Custom manager for the CustomUser model.

    Provides methods to create regular users and superusers.
    """

    def create_user(self, username, email, password, **extra_fields):
        """
        Creates and saves a regular user.

        Args:
            username (str): The username of the user.
            email (str): The email address of the user.
            password (str): The user's password.
            **extra_fields: Additional fields for the user model.

        Returns:
            CustomUser: The created user instance.
        """
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        """
        Creates and saves a superuser.

        Automatically sets 'is_staff', 'is_superuser', and 'is_active' to True.

        Args:
            username (str): The username of the superuser.
            email (str): The email address of the superuser.
            password (str): The superuser's password.
            **extra_fields: Additional fields for the user model.

        Returns:
            CustomUser: The created superuser instance.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(username=username, email=email, password=password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model extending AbstractBaseUser and PermissionsMixin.

    Fields:
        - username: Unique username for authentication.
        - email: Unique email address.
        - type: User type ('business', 'customer', 'superuser').
        - is_guest: Indicates if the user is a guest.
        - is_active: Whether the user is active.
        - is_staff: Whether the user has staff privileges.
        - created_at: Timestamp when the user was created.
        - updated_at: Timestamp when the user was last updated.
    """
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(unique=True, null=False, blank=False)
    type = models.CharField(max_length=32, choices=[('business', 'Business'), ('customer', 'Customer'), ('superuser', 'Superuser')])
    is_guest = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        """
        String representation of the user.
        """
        return f"{self.username}"

    class Meta:
        verbose_name = "account"
        """
        Human-readable name for the model in admin and elsewhere.
        """
