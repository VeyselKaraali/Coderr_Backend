from django.urls import reverse
from rest_framework import serializers
from app_offers.models import Offer, Detail

REQUIRED_DETAILS_COUNT = 3


class DetailSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating Detail objects.

    Fields:
        - id: Detail ID
        - title: Title of the detail
        - revisions: Number of revisions included
        - delivery_time_in_days: Delivery time in days
        - price: Price of the detail
        - features: Additional features
        - offer_type: Type of offer (used to differentiate details)
    """

    class Meta:
        model = Detail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']


class DetailReadOnlySerializer(serializers.ModelSerializer):
    """
    Read-only serializer for Detail objects with URL reference.

    Fields:
        - id: Detail ID
        - url: URL to access detail via API
    """
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        """
        Returns the API URL for a given detail instance.
        """
        return reverse('offer_details', args=[obj.pk])

    class Meta:
        model = Detail
        fields = ['id', 'url']


class OfferCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating or updating Offer objects along with associated Details.

    Validates that exactly REQUIRED_DETAILS_COUNT details are provided on creation.
    Handles creation, update, and partial update of nested Detail objects.
    """
    details = DetailSerializer(many=True)

    def validate_details(self, value):
        """
        Validates the number of details during creation.
        """
        if self.instance is None and len(value) != REQUIRED_DETAILS_COUNT:
            raise serializers.ValidationError(f"Offer must have exactly {REQUIRED_DETAILS_COUNT} details.")
        return value

    def create(self, validated_data):
        """
        Creates a new Offer and associated Detail objects.
        """
        details_data = validated_data.pop('details', [])
        offer = Offer.objects.create(user=self.context['request'].user, **validated_data)

        for detail_data in details_data:
            Detail.objects.create(offer=offer, **detail_data)

        return offer

    def update(self, instance, validated_data):
        """
        Updates an existing Offer and its associated Detail objects.
        - Updates existing details based on 'offer_type'.
        - Creates new details if they do not exist.
        """
        details_data = validated_data.pop('details', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data is not None:
            existing_details_map = {detail.offer_type: detail for detail in instance.details.all()}

            for detail_data in details_data:
                offer_type = detail_data.get('offer_type', None)

                if offer_type and offer_type in existing_details_map:
                    detail_instance = existing_details_map[offer_type]

                    detail_data.pop('id', None)

                    for key, value in detail_data.items():
                        setattr(detail_instance, key, value)
                    detail_instance.save()

                else:
                    detail_data.pop('id', None)
                    Detail.objects.create(offer=instance, **detail_data)

        return instance

    class Meta:
        model = Offer
        fields = [
            'title',
            'image',
            'description',
            'details'
        ]


class OfferReadOnlySerializer(serializers.ModelSerializer):
    """
    Read-only serializer for Offer objects including nested Detail objects.
    """
    details = DetailSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id',
            'title',
            'image',
            'description',
            'details',
        ]


class OfferSerializer(serializers.ModelSerializer):
    """
    Serializer for Offer objects with additional read-only fields:
    - details (nested)
    - min_price
    - min_delivery_time
    - user_details (first name, last name, username)
    """
    details = DetailReadOnlySerializer(many=True, read_only=True)
    min_price = serializers.DecimalField(max_digits=16, decimal_places=2, read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id',
            'user',
            'title',
            'image',
            'description',
            'created_at',
            'updated_at',
            'details',
            'min_price',
            'min_delivery_time',
            'user_details'
        ]

    def get_user_details(self, obj):
        """
        Retrieves user profile information (first name, last name, username) for the offer.
        Returns empty strings if the profile does not exist.
        """
        profile = getattr(obj.user, 'profile', None)

        return {
            'first_name': profile.first_name if profile else '',
            'last_name': profile.last_name if profile else '',
            'username': obj.user.username
        }
