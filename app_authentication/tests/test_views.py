from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class BaseAuthTestCase(APITestCase):
    REGISTRATION_DATA = {
        'username': 'test_user',
        'email': 'test@example.com',
        'password': 'pass123',
        'type': 'CUSTOMER',
    }

    LOGIN_DATA = {
        'username': 'test_user',
        'password': 'pass123',
    }

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.registration_url = reverse('registration')
        cls.login_url = reverse('login')
        cls.logout_url = reverse('logout')
        cls.token_refresh_url = reverse('token_refresh')

    @staticmethod
    def get_registration_data(overrides=None):
        data = {
            'username': 'new_user',
            'email': 'new@example.com',
            'password': 'pass123',
            'repeated_password': 'pass123',
            'type': 'CUSTOMER',
        }
        if overrides:
            data.update(overrides)
        return data


class RegistrationViewTests(BaseAuthTestCase):
    def test_registration_success(self):
        response = self.client.post(self.registration_url, self.get_registration_data())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertTrue(User.objects.filter(username='new_user').exists())

    def test_registration_password_mismatch(self):
        data = self.get_registration_data({'repeated_password': 'wrong_pass'})
        response = self.client.post(self.registration_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTests(BaseAuthTestCase):
    def setUp(self):
        self.user = User.objects.create_user(**self.REGISTRATION_DATA)

    def test_login_success(self):
        response = self.client.post(self.login_url, self.LOGIN_DATA)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_invalid_credentials(self):
        invalid_data = {**self.LOGIN_DATA, 'password': 'wrong_pass'}
        response = self.client.post(self.login_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_successful_token_refresh(self):
        login_resp = self.client.post(self.login_url, self.LOGIN_DATA)
        refresh_token = login_resp.data['refresh']
        old_access_token = login_resp.data['access']

        response = self.client.post(self.token_refresh_url, {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertNotEqual(response.data['access'], old_access_token)

    def test_throttle_limit(self):
        from app_authentication.api.views import LoginThrottle
        throttle = LoginThrottle()
        num_requests, _ = throttle.parse_rate(throttle.rate)

        invalid_data = {**self.LOGIN_DATA, 'password': 'wrong_pass'}
        for _ in range(num_requests):
            self.client.post(self.login_url, invalid_data)
        response = self.client.post(self.login_url, invalid_data)

        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class LogoutViewTests(BaseAuthTestCase):
    def setUp(self):
        self.user = User.objects.create_user(**self.REGISTRATION_DATA)
        self.refresh_token = str(RefreshToken.for_user(self.user))

    def authenticate(self):
        self.client.force_authenticate(user=self.user)

    def test_logout_success(self):
        self.authenticate()
        response = self.client.post(self.logout_url, {'refresh': self.refresh_token})
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_logout_missing_token(self):
        self.authenticate()
        response = self.client.post(self.logout_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_invalid_token(self):
        self.authenticate()
        response = self.client.post(self.logout_url, {'refresh': 'invalidtoken'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_and_blacklist_token(self):
        # ToDo
        login_resp = self.client.post(self.login_url, self.LOGIN_DATA)
        access_token = login_resp.data['access']
        refresh_token = login_resp.data['refresh']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        logout_response = self.client.post(self.logout_url, {'refresh': refresh_token})
        self.assertEqual(logout_response.status_code, status.HTTP_205_RESET_CONTENT)

        refresh_response = self.client.post(self.token_refresh_url, {'refresh': refresh_token})
        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)