from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class RegistrationViewTests(APITestCase):
    def get_registration_data(self, **kwargs):
        data = {
            'username': 'newuser',
            'email': 'test@example.com',
            'password': 'pass123',
            'password_repeat': 'pass123',
            'type': 'CUSTOMER',
        }
        data.update(kwargs)
        return data

    def test_registration_success(self):
        response = self.client.post(reverse('registration'), self.get_registration_data())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)

    def test_registration_password_mismatch(self):
        data = self.get_registration_data(password_repeat='wrongpass')
        response = self.client.post(reverse('registration'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='loginuser',
            password='pass123',
            email='test@test.com',
            type='CUSTOMER'
        )

    def get_login_data(self, **kwargs):
        data = {
            'username': 'loginuser',
            'password': 'pass123',
        }
        data.update(kwargs)
        return data

    def test_login_success(self):
        response = self.client.post(reverse('login'), self.get_login_data())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('login'), self.get_login_data(password='wrong'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_throttle_limit(self):
        data = self.get_login_data(password='wrong')
        for _ in range(6):
            self.client.post(reverse('login'), data)
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class LogoutViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='logoutuser',
            password='pass123',
            email='test@test.com',
            type='CUSTOMER'
        )
        self.refresh = str(RefreshToken.for_user(self.user))

    def test_logout_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('logout'), {'refresh': self.refresh})
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_logout_missing_token(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('logout'), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_invalid_token(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('logout'), {'refresh': 'invalidtoken'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)