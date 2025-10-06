import pytest
from rest_framework.exceptions import ValidationError
from app_authentication.api.serializers import RegistrationSerializer, RegistrationGuestSerializer, LoginSerializer
from app_authentication.models import CustomUser

@pytest.mark.django_db
class TestAuthSerializers:

    @pytest.fixture
    def user_data(self):
        return {
            "username": "user",
            "email": "user@test.com",
            "password": "Password123!",
            "repeated_password": "Password123!",
            "type": "customer",
            "is_guest": False
        }

    def test_registration_serializer_valid(self, user_data):
        serializer = RegistrationSerializer(data=user_data)
        assert serializer.is_valid()
        user = serializer.save()
        assert user.username == user_data["username"]
        assert user.email == user_data["email"]
        assert not user.is_guest
        assert user.check_password(user_data["password"])

    def test_registration_serializer_password_mismatch(self, user_data):
        user_data["repeated_password"] = "WrongPassword"
        serializer = RegistrationSerializer(data=user_data)
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_guest_serializer_creates_guest(self):
        serializer = RegistrationGuestSerializer(data={"type": "customer", "is_guest": True})
        assert serializer.is_valid()
        guest = serializer.save()
        assert guest.is_guest
        assert guest.username.startswith("Guest_")
        assert guest.email.startswith("guest_")
        assert not guest.has_usable_password()

    def test_login_serializer_valid(self):
        user = CustomUser.objects.create_user(username="user1", email="user1@test.com", password="Password123!")
        serializer = LoginSerializer(data={"username": "user1", "password": "Password123!"})
        assert serializer.is_valid()
        validated_data = serializer.validated_data
        assert validated_data["user"] == user

    def test_login_serializer_invalid(self):
        serializer = LoginSerializer(data={"username": "wrong", "password": "abc"})
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)
