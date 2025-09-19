from django.db import models
from django.conf import settings


class Offer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="offers")
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="offers/", null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def min_price(self):
        detail = self.details.order_by("price").first()
        return detail.price if detail else None

    @property
    def min_delivery_time(self):
        detail = self.details.order_by("delivery_time_in_days").first()
        return detail.delivery_time_in_days if detail else None

    def __str__(self):
        return self.title


