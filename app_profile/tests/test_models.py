import pytest
from app_authentication.models import CustomUser
from app_profile.models import Profile

@pytest.mark.django_db
class TestProfileModel:

    @pytest.fixture
    def users(self):
        customer = CustomUser.objects.create_user(
            username="customer",
            email="customer@test.com",
            password="password123",
            type="customer"
        )
        business = CustomUser.objects.create_user(
            username="business",
            email="business@test.com",
            password="password123",
            type="business"
        )
        return customer, business

    @pytest.fixture
    def profiles(self, users):
        customer, business = users
        profile_customer = Profile.objects.create(user=customer, first_name="John", last_name="Doe")
        profile_business = Profile.objects.create(user=business, first_name="Alice", last_name="Smith", location="Berlin")
        return profile_customer, profile_business

    def test_profile_str(self, profiles):
        profile_customer, profile_business = profiles
        assert str(profile_customer) == "customer"
        assert str(profile_business) == "business"

    def test_profile_default_values(self, users):
        customer, _ = users
        profile = Profile.objects.create(user=customer)
        assert profile.first_name == ""
        assert profile.last_name == ""
        assert profile.location == ""
        assert profile.tel == ""
        assert profile.description == ""
        assert profile.working_hours == ""

    def test_profile_field_assignment(self, profiles):
        profile_customer, profile_business = profiles
        assert profile_customer.first_name == "John"
        assert profile_customer.last_name == "Doe"
        assert profile_business.location == "Berlin"
