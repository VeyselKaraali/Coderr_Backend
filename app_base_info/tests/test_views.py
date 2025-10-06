import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from app_reviews.models import Review
from app_authentication.models import CustomUser
from app_offers.models import Offer


@pytest.mark.django_db
class TestBaseInfoView:

    @pytest.fixture
    def client(self):
        return APIClient()

    def test_returns_empty_counts(self, client):
        url = reverse("base-info")
        response = client.get(url)

        assert response.status_code == 200
        data = response.json()
        assert data["review_count"] == 0
        assert data["average_rating"] == 0.0
        assert data["business_profile_count"] == 0
        assert data["offer_count"] == 0

    def test_returns_correct_counts_and_average(self):
        client = APIClient()

        business_user = CustomUser.objects.create(username="business", email="business_user@test.com", type="business")

        reviewer1 = CustomUser.objects.create(username="customer1", email="customer1@test.com", type="customer")
        reviewer2 = CustomUser.objects.create(username="customer2", email="customer2@test.com", type="customer")

        Offer.objects.create(user=business_user, title="Offer 1", description="Desc 1")
        Offer.objects.create(user=business_user, title="Offer 2", description="Desc 2")

        Review.objects.create(business_user=business_user, reviewer=reviewer1, rating=4, description="Desc 1")
        Review.objects.create(business_user=business_user, reviewer=reviewer2, rating=2, description="Desc 2")

        response = client.get("/api/base-info/")
        assert response.status_code == 200

        data = response.json()
        assert data["business_profile_count"] == 1
        assert data["offer_count"] == 2
        assert data["review_count"] == 2
        assert data["average_rating"] == 3.0




