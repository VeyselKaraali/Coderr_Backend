from rest_framework import serializers

from app_offers.models import Detail
from app_orders.models import Order


class OrderCreateSerializer(serializers.Serializer):
    """
    Serializer for creating an Order from an offer detail.

    Fields:
        - offer_detail_id: Integer ID of the Detail to create the order from.
    """
    offer_detail_id = serializers.IntegerField()

    def validate_offer_detail_id(self, value):
        """
        Validates that the given offer_detail_id exists in the database.

        Raises:
            serializers.ValidationError: If the Detail with the given ID does not exist.
        """
        if not Detail.objects.filter(id=value).exists():
            raise serializers.ValidationError("Detail with this ID does not exist.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order objects, including all relevant fields for display.

    Fields:
        - id: Order ID
        - customer_user: The user who placed the order
        - business_user: The business user providing the offer
        - title: Title of the order/detail
        - revisions: Number of revisions included
        - delivery_time_in_days: Delivery time in days
        - price: Price of the order
        - features: Additional features of the order
        - offer_type: Type of the offer (basic, standard, premium)
        - status: Current status of the order
        - created_at: Timestamp when the order was created
        - updated_at: Timestamp when the order was last updated
    """
    class Meta:
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]
