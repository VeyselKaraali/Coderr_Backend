from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models


class UserManager(BaseUserManager):
    MIN_PASSWORD_LENGTH = 6

    def validate_password_length(self, password):
        if len(password) < self.MIN_PASSWORD_LENGTH:
            raise ValidationError(
                f'Password must be at least {self.MIN_PASSWORD_LENGTH} characters long.'
            )

    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set.')

        if email:
            email = self.normalize_email(email)

        if password:
            self.validate_password_length(password)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(username, password, **extra_fields)


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        abstract = True

    username = models.CharField(max_length=32, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
