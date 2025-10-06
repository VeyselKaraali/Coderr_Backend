import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from app_authentication.models import CustomUser as User
from app_profile.models import Profile

@pytest.fixture
def users(db):
    customer = User.objects.create_user(username="customer1", email="customer1@test.com", password="testpass123", type="customer")
    business = User.objects.create_user(username="business1", email="business1@test.com", password="testpass123", type="business")
    return customer, business

@pytest.fixture
def profiles(db, users):
    customer, business = users
    profile_customer = Profile.objects.create(user=customer, first_name="Customer", last_name="One")
    profile_business = Profile.objects.create(user=business, first_name="Business", last_name="One", location="Berlin")
    return profile_customer, profile_business

@pytest.fixture
def client_customer(users):
    client = APIClient()
    client.force_authenticate(user=users[0])
    return client

@pytest.fixture
def client_business(users):
    client = APIClient()
    client.force_authenticate(user=users[1])
    return client

class TestProfileViews:

    def test_profile_detail_get(self, client_customer, profiles):
        profile_customer, profile_business = profiles
        url = reverse('profile_detail', args=[profile_customer.id])
        response = client_customer.get(url)
        assert response.status_code == 200
        data = response.data
        assert data['first_name'] == profile_customer.first_name
        assert data['last_name'] == profile_customer.last_name
        assert data['username'] == profile_customer.user.username

    def test_profile_detail_patch(self, client_customer, profiles):
        profile_customer, _ = profiles
        url = reverse('profile_detail', args=[profile_customer.id])
        response = client_customer.patch(url, {"first_name": "Updated"}, format='json')
        assert response.status_code == 200
        profile_customer.refresh_from_db()
        assert profile_customer.first_name == "Updated"

    def test_profile_business_list(self, client_business, profiles):
        _, profile_business = profiles
        url = reverse('profile_business')
        response = client_business.get(url)
        assert response.status_code == 200
        data = response.data
        assert any(p['username'] == profile_business.user.username for p in data)

    def test_profile_customer_list(self, client_customer, profiles):
        profile_customer, _ = profiles
        url = reverse('profile_customer')
        response = client_customer.get(url)
        assert response.status_code == 200
        data = response.data
        assert any(p['username'] == profile_customer.user.username for p in data)
