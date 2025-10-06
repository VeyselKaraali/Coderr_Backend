import pytest
from rest_framework.exceptions import ValidationError
from app_offers.models import Offer, Detail
from app_offers.api.serializers import (
    OfferCreateUpdateSerializer,
    OfferReadOnlySerializer,
    OfferSerializer,
    DetailSerializer,
    DetailReadOnlySerializer
)
from app_authentication.models import CustomUser
from django.urls import reverse

@pytest.mark.django_db
class TestOfferSerializers:

    @pytest.fixture
    def user(self):
        return CustomUser.objects.create(username="biz1", email="biz1@test.com", type="business")

    @pytest.fixture
    def offer(self, user):
        offer = Offer.objects.create(user=user, title="Test Offer", description="Desc")
        Detail.objects.create(offer=offer, title="Basic", revisions=1, delivery_time_in_days=3, price=10, features=[], offer_type="basic")
        Detail.objects.create(offer=offer, title="Standard", revisions=2, delivery_time_in_days=2, price=20, features=[], offer_type="standard")
        Detail.objects.create(offer=offer, title="Premium", revisions=3, delivery_time_in_days=1, price=30, features=[], offer_type="premium")
        return offer

    def test_detail_serializer(self, offer):
        detail = offer.details.first()
        serializer = DetailSerializer(detail)
        data = serializer.data
        assert data['title'] == detail.title
        assert data['price'] == str(detail.price)

    def test_detail_read_only_serializer(self, offer):
        detail = offer.details.first()
        serializer = DetailReadOnlySerializer(detail)
        data = serializer.data
        assert data['id'] == detail.id
        assert data['url'] == reverse('offer_details', args=[detail.id])

    def test_offer_create_update_serializer_valid(self, user):
        data = {
            "title": "New Offer",
            "description": "Test desc",
            "details": [
                {"title": "Basic", "revisions": 1, "delivery_time_in_days": 1, "price": 5, "features": [], "offer_type": "basic"},
                {"title": "Standard", "revisions": 1, "delivery_time_in_days": 2, "price": 10, "features": [], "offer_type": "standard"},
                {"title": "Premium", "revisions": 1, "delivery_time_in_days": 3, "price": 15, "features": [], "offer_type": "premium"},
            ]
        }
        serializer = OfferCreateUpdateSerializer(data=data, context={"request": type("Req", (), {"user": user})()})
        assert serializer.is_valid(), serializer.errors
        offer = serializer.save()
        assert Offer.objects.filter(id=offer.id).exists()
        assert offer.details.count() == 3

    def test_offer_create_update_serializer_invalid_detail_count(self, user):
        data = {
            "title": "New Offer",
            "description": "Test desc",
            "details": [
                {"title": "Basic", "revisions": 1, "delivery_time_in_days": 1, "price": 5, "features": [], "offer_type": "basic"},
            ]
        }
        serializer = OfferCreateUpdateSerializer(data=data, context={"request": type("Req", (), {"user": user})()})
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_offer_read_only_serializer(self, offer):
        serializer = OfferReadOnlySerializer(offer)
        data = serializer.data
        assert data['id'] == offer.id
        assert len(data['details']) == 3

    def test_offer_serializer_min_fields(self, offer):
        serializer = OfferSerializer(offer)
        data = serializer.data
        assert data['id'] == offer.id
        assert float(data['min_price']) == 10.0
        assert data['min_delivery_time'] == 1
        assert 'user_details' in data
        assert data['user_details']['username'] == offer.user.username
        assert data['user_details']['first_name'] == ''
        assert data['user_details']['last_name'] == ''
