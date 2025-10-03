from rest_framework import serializers

from app_orders.models import Order

class OrderCreateSerializer(serializers.Serializer):
    offer_detail_id = serializers.IntegerField()

class OrderSerializer(serializers.ModelSerializer):
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