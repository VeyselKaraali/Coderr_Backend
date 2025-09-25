from django.urls import reverse
from rest_framework import serializers
from app_offers.models import Offer, OfferDetail, Feature

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'offer_detail', 'name']


