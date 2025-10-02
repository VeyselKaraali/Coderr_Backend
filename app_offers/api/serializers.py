from django.urls import reverse
from rest_framework import serializers
from app_offers.models import Offer, Detail

REQUIRED_DETAILS_COUNT = 3

class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']


class DetailReadOnlySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return reverse('offer_details', args=[obj.pk])

    class Meta:
        model = Detail
        fields = ['id', 'url']


class OfferCreateUpdateSerializer(serializers.ModelSerializer):
    details = DetailSerializer(many=True)

    def validate_details(self, value):
        if self.instance is None and len(value) != REQUIRED_DETAILS_COUNT:
            raise serializers.ValidationError(f"Offer must have exactly {REQUIRED_DETAILS_COUNT} details.")
        return value

    def create(self, validated_data):
        details_data = validated_data.pop('details', [])
        offer = Offer.objects.create(user=self.context['request'].user, **validated_data)

        for detail_data in details_data:
            Detail.objects.create(offer=offer, **detail_data)

        return offer

    def update(self, instance, validated_data):
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
    details = DetailReadOnlySerializer(many=True, read_only=True)
    min_price = serializers.DecimalField(max_digits=16, decimal_places=2,read_only=True)
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
        profile = getattr(obj.user, 'profile', None)
        if profile:
            return {
                'first_name': profile.first_name,
                'last_name': profile.last_name,
                'username': obj.user.username
            }


