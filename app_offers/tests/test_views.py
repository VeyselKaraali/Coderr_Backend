import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from app_authentication.models import CustomUser
from app_offers.models import Offer, Detail


@pytest.mark.django_db
class TestOfferViews:

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def business_user(self):
        return CustomUser.objects.create(username="business", email="business@test.com", type="business")

    @pytest.fixture
    def customer_user(self):
        return CustomUser.objects.create(username="customer", email="customer@test.com", type="customer")

    @pytest.fixture
    def offer(self, business_user):
        offer = Offer.objects.create(user=business_user, title="Test Offer", description="Desc")
        Detail.objects.create(offer=offer, title="Basic", revisions=1, delivery_time_in_days=3, price=10, features=[], offer_type="basic")
        Detail.objects.create(offer=offer, title="Standard", revisions=2, delivery_time_in_days=2, price=20, features=[], offer_type="standard")
        Detail.objects.create(offer=offer, title="Premium", revisions=3, delivery_time_in_days=1, price=30, features=[], offer_type="premium")
        return offer

    def test_get_offers_list(self, client, offer):
        url = reverse("offers")
        response = client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert data['results'][0]['title'] == "Test Offer"

    def test_post_offer_requires_business_user(self, client, business_user, customer_user):
        client.force_authenticate(user=customer_user)
        url = reverse("offers")
        response = client.post(url, data={"title": "New Offer", "description": "Desc", "details": []}, format="json")
        assert response.status_code == 403

        client.force_authenticate(user=business_user)
        response = client.post(url, data={"title": "New Offer", "description": "Desc", "details": [
            {"title": "Basic", "revisions": 1, "delivery_time_in_days": 1, "price": 5, "features": [], "offer_type": "basic"},
            {"title": "Standard", "revisions": 1, "delivery_time_in_days": 2, "price": 10, "features": [], "offer_type": "standard"},
            {"title": "Premium", "revisions": 1, "delivery_time_in_days": 3, "price": 15, "features": [], "offer_type": "premium"},
        ]}, format="json")
        assert response.status_code == 201
        assert Offer.objects.filter(title="New Offer").exists()

    def test_get_offer_detail(self, client, offer, customer_user):
        client.force_authenticate(user=customer_user)
        url = reverse("offer", args=[offer.id])
        response = client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == offer.id

    def test_patch_offer_by_owner(self, client, offer, business_user):
        client.force_authenticate(user=business_user)
        url = reverse("offer", args=[offer.id])
        response = client.patch(url, data={"title": "Updated Title"}, format="json")
        assert response.status_code == 200
        offer.refresh_from_db()
        assert offer.title == "Updated Title"

    def test_delete_offer_by_owner(self, client, offer, business_user):
        client.force_authenticate(user=business_user)
        url = reverse("offer", args=[offer.id])
        response = client.delete(url)
        assert response.status_code == 204
        assert not Offer.objects.filter(id=offer.id).exists()

    def test_get_offer_detail_view(self, client, offer, customer_user):
        client.force_authenticate(user=customer_user)
        detail_id = offer.details.first().id
        url = reverse("offer_details", args=[detail_id])
        response = client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == detail_id
