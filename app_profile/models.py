from django.db import models
from app_authentication.models import Account, AccountType
from core.models import TimeStamped
from django.db.models import Q

class Profile(TimeStamped):
    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        limit_choices_to=~Q(type=AccountType.SUPERUSER),
        related_name='profile'
    )
    first_name = models.CharField(max_length=32, blank=True, default='')
    last_name = models.CharField(max_length=32, blank=True, default='')
    file = models.FileField(null=True, blank=True)
    location = models.CharField(max_length=64, blank=True, default='')
    tel = models.CharField(max_length=32, blank=True, default='')
    description = models.TextField(blank=True, default='')
    working_hours = models.CharField(max_length=64, blank=True, default='')

    def __str__(self):
        return f"{self.account.username}"

