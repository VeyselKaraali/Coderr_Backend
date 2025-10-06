from django.db import models
from app_authentication.models import CustomUser


class Profile(models.Model):
    """
    Model representing a user profile with additional information.

    Fields:
        - user: One-to-one relation with the CustomUser model.
        - first_name: First name of the user (optional).
        - last_name: Last name of the user (optional).
        - file: Optional file associated with the profile.
        - location: Location or address of the user or business (optional).
        - tel: Contact telephone number (optional).
        - description: Additional description or bio (optional).
        - working_hours: Working hours (for business users) (optional).
        - created_at: Timestamp when the profile was created.
        - updated_at: Timestamp when the profile was last updated.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=32, blank=True, default='')
    last_name = models.CharField(max_length=32, blank=True, default='')
    file = models.FileField(blank=True)
    location = models.CharField(max_length=64, blank=True, default='')
    tel = models.CharField(max_length=32, blank=True, default='')
    description = models.TextField(blank=True, default='')
    working_hours = models.CharField(max_length=64, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns the username of the related user as string representation.
        """
        return f"{self.user.username}"
