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


class OfferDetail(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="details")
    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=16, decimal_places=2)
    OFFER_TYPES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]
    offer_type = models.CharField(max_length=32, choices=OFFER_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.offer.title} – {self.title} ({self.offer_type})"


class Feature(models.Model):
    offer_detail = models.ForeignKey(OfferDetail, on_delete=models.CASCADE, related_name="features")
    name = models.CharField(max_length=255)
