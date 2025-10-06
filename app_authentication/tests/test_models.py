import pytest
from app_authentication.models import CustomUser

@pytest.mark.django_db
class TestCustomUserModel:

    def test_create_user(self):
        user = CustomUser.objects.create_user(
            username="user",
            email="user@test.com",
            password="Password123!",
            type="customer"
        )
        assert user.username == "user"
        assert user.email == "user@test.com"
        assert user.type == "customer"
        assert not user.is_staff
        assert not user.is_superuser
        assert not user.is_guest
        assert user.check_password("Password123!")

    def test_create_superuser(self):
        superuser = CustomUser.objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="AdminPass123!"
        )
        assert superuser.is_staff
        assert superuser.is_superuser
        assert superuser.is_active
        assert superuser.check_password("AdminPass123!")

    def test_guest_user_flag(self):
        guest = CustomUser.objects.create_user(
            username="guest",
            email="guest@test.com",
            password="GuestPass123!",
            type="customer",
            is_guest=True
        )
        assert guest.is_guest
        assert guest.username == "guest"
        assert guest.email == "guest@test.com"

    def test_str_method(self):
        user = CustomUser.objects.create_user(
            username="user",
            email="user@test.com",
            password="Password123!",
            type="business"
        )
        assert str(user) == "user"
