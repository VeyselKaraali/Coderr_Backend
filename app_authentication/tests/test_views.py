import pytest
from rest_framework.test import APIClient
from app_authentication.models import CustomUser
from rest_framework.authtoken.models import Token

@pytest.mark.django_db
class TestAuthViews:

    @pytest.fixture
    def client(self):
        return APIClient()

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

    @pytest.fixture
    def guest_data(self):
        return {"type": "customer", "is_guest": True}

    def test_registration_regular_user(self, client, user_data):
        response = client.post("/api/registration/", user_data, format="json")
        assert response.status_code == 201
        assert "token" in response.data
        user = CustomUser.objects.get(username="user")
        assert user.email == "user@test.com"
        assert not user.is_guest

    def test_registration_guest_user(self, client, guest_data):
        response = client.post("/api/registration/", guest_data, format="json")
        assert response.status_code == 201
        assert response.data["username"].startswith("Guest_")
        user = CustomUser.objects.get(username=response.data["username"])
        assert user.is_guest

    def test_registration_password_mismatch(self, client, user_data):
        user_data["repeated_password"] = "WrongPassword"
        response = client.post("/api/registration/", user_data, format="json")
        assert response.status_code == 400
        assert "repeated_password" in response.data

    def test_login_success(self, client, user_data):
        client.post("/api/registration/", user_data, format="json")
        response = client.post("/api/login/", {"username": "user", "password": "Password123!"}, format="json")
        assert response.status_code == 200
        assert "token" in response.data

    def test_login_failure(self, client):
        response = client.post("/api/login/", {"username": "nonexistent", "password": "abc"}, format="json")
        assert response.status_code == 400

    def test_logout(self, client, user_data):
        client.post("/api/registration/", user_data, format="json")
        token = Token.objects.get(user__username="user")
        client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        response = client.post("/api/logout/")
        assert response.status_code == 205
        assert not Token.objects.filter(user__username="user1").exists()
