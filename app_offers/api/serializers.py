from django.urls import reverse
from rest_framework import serializers
from app_offers.models import Offer, Detail


class DetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']





