from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

User = get_user_model()

class UserModelTests(APITestCase):
    def setUp(self):
        self.registration_url = reverse('registration')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.refresh_url = reverse('token_refresh')

        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'pass123',
            'password_repeat': 'pass123',
            'type': 'CUSTOMER',
            'is_guest': False,
            'is_superuser': False,
            'is_staff': False,
        }

    def create_user(self, **kwargs):
        defaults = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'pass123',
            'type': 'CUSTOMER',
            'is_guest': False,
            'is_superuser': False,
            'is_staff': False,
        }
        defaults.update(kwargs)
        return User(**defaults)