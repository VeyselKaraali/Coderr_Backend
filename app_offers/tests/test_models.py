import pytest
from django.contrib.auth import get_user_model
from app_offers.models import Offer, Detail

User = get_user_model()


@pytest.mark.django_db
class TestOfferModels:

    @pytest.fixture
    def user(self):
        return User.objects.create(username="testuser", email="test@test.com", type="business")

    @pytest.fixture
    def offer(self, user):
        return Offer.objects.create(user=user, title="Test Offer", description="Description")

    @pytest.fixture
    def details(self, offer):
        return [
            Detail.objects.create(
                offer=offer,
                title="Basic",
                revisions=1,
                delivery_time_in_days=5,
                price=10.0,
                features=[],
                offer_type="basic"
            ),
            Detail.objects.create(
                offer=offer,
                title="Standard",
                revisions=2,
                delivery_time_in_days=3,
                price=20.0,
                features=[],
                offer_type="standard"
            ),
            Detail.objects.create(
                offer=offer,
                title="Premium",
                revisions=3,
                delivery_time_in_days=1,
                price=30.0,
                features=[],
                offer_type="premium"
            ),
        ]

    def test_min_price_and_delivery_time(self, offer, details):
        assert offer.min_price == 10.0
        assert offer.min_delivery_time == 1

    def test_offer_str(self, offer):
        assert str(offer) == "Test Offer"

    def test_detail_str(self, offer):
        detail = Detail.objects.create(
            offer=offer,
            title="Test Detail",
            revisions=1,
            delivery_time_in_days=2,
            price=15.0,
            features=[],
            offer_type="basic"
        )
        assert str(detail) == f"Test Offer – Test Detail (basic)"

    def test_offer_details_relationship(self, offer, details):
        assert offer.details.count() == 3
        titles = [d.title for d in offer.details.all()]
        assert "Basic" in titles
        assert "Standard" in titles
        assert "Premium" in titles
