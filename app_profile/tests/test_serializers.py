import pytest
from app_authentication.models import CustomUser as User
from app_profile.models import Profile
from app_profile.api.serializers import (
    ProfileSerializer,
    BusinessProfileSerializer,
    CustomerProfileSerializer,
    ProfileDetailSerializer,
)

@pytest.fixture
def users(db):
    customer = User.objects.create_user(username="customer", email="customer@test.com", password="testpass123", type="customer")
    business = User.objects.create_user(username="business", email="business@test.com", password="testpass123", type="business")
    return customer, business

@pytest.fixture
def profiles(db, users):
    customer, business = users
    profile_customer = Profile.objects.create(user=customer, first_name="Customer", last_name="One")
    profile_business = Profile.objects.create(user=business, first_name="Business", last_name="One", location="Berlin")
    return profile_customer, profile_business

class TestProfileSerializers:

    def test_profile_serializer_basic_fields(self, profiles):
        profile_customer, _ = profiles
        serializer = ProfileSerializer(profile_customer)
        data = serializer.data
        assert data['user'] == profile_customer.user.id
        assert data['username'] == profile_customer.user.username
        assert data['first_name'] == profile_customer.first_name
        assert data['last_name'] == profile_customer.last_name
        assert data['is_guest'] == profile_customer.user.is_guest
        assert data['type'] == profile_customer.user.type

    def test_business_profile_serializer_fields(self, profiles):
        _, profile_business = profiles
        serializer = BusinessProfileSerializer(profile_business)
        data = serializer.data
        assert data['username'] == profile_business.user.username
        assert data['first_name'] == profile_business.first_name
        assert 'location' in data
        assert 'tel' in data
        assert 'description' in data
        assert 'working_hours' in data

    def test_customer_profile_serializer_fields(self, profiles):
        profile_customer, _ = profiles
        serializer = CustomerProfileSerializer(profile_customer)
        data = serializer.data
        assert data['username'] == profile_customer.user.username
        assert data['first_name'] == profile_customer.first_name
        assert 'location' not in data
        assert 'tel' not in data

    def test_profile_detail_serializer_fields(self, profiles):
        _, profile_business = profiles
        serializer = ProfileDetailSerializer(profile_business)
        data = serializer.data
        assert data['username'] == profile_business.user.username
        assert data['location'] == profile_business.location
        assert 'email' in data
        assert data['email'] == profile_business.user.email
        assert 'created_at' in data
        assert 'updated_at' in data
