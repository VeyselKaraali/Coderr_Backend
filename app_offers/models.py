from django.db import models
from django.conf import settings


class Offer(models.Model):
    """
    Model representing an offer created by a user.

    Fields:
        - user: ForeignKey to the user who created the offer.
        - title: Title of the offer.
        - image: Optional image for the offer.
        - description: Detailed description of the offer.
        - created_at: Timestamp when the offer was created.
        - updated_at: Timestamp when the offer was last updated.

    Properties:
        - min_price: Returns the minimum price among associated details.
        - min_delivery_time: Returns the minimum delivery time among associated details.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="offers")
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="offers/", null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def min_price(self):
        """
        Returns the lowest price from the associated details.
        """
        detail = self.details.order_by("price").first()
        return detail.price if detail else None

    @property
    def min_delivery_time(self):
        """
        Returns the shortest delivery time (in days) from the associated details.
        """
        detail = self.details.order_by("delivery_time_in_days").first()
        return detail.delivery_time_in_days if detail else None

    def __str__(self):
        """
        String representation of the offer.
        """
        return self.title


class Detail(models.Model):
    """
    Model representing a specific detail or tier of an offer.

    Fields:
        - offer: ForeignKey to the related offer.
        - title: Title of the detail.
        - revisions: Number of revisions included in this detail.
        - delivery_time_in_days: Delivery time in days.
        - price: Price for this detail.
        - features: JSON list of additional features.
        - offer_type: Type of detail (basic, standard, premium).
        - created_at: Timestamp when the detail was created.
    """
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="details")
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=16, decimal_places=2)
    features = models.JSONField(default=list)
    OFFER_TYPES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]
    offer_type = models.CharField(max_length=32, choices=OFFER_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the detail, including offer title and type.
        """
        return f"{self.offer.title} – {self.title} ({self.offer_type})"
