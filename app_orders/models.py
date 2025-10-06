from django.db import models
from core import settings


class Order(models.Model):
    """
    Model representing a customer order for a specific offer detail.

    Fields:
        - customer_user: ForeignKey to the user placing the order.
        - business_user: ForeignKey to the business user providing the offer.
        - title: Title of the order/detail.
        - revisions: Number of revisions included in the order.
        - delivery_time_in_days: Delivery time in days.
        - price: Price of the order.
        - features: List of additional features (stored as JSON).
        - offer_type: Type of the offer (e.g., basic, standard, premium).
        - status: Current status of the order ('in_progress', 'completed', 'cancelled').
        - created_at: Timestamp when the order was created.
        - updated_at: Timestamp when the order was last updated.
    """
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders_customer')
    business_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders_business')
    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField(default=0)
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=16, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=64)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns a string representation of the order, including its ID and title.
        """
        return f"Order {self.id} - {self.title}"
