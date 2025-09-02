from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.test import APITestCase

from app_authentication.api.serializers import LoginSerializer, RegistrationSerializer


User = get_user_model()

class RegistrationSerializerTests(APITestCase):
    def get_valid_data(self, **kwargs):
        data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'pass123',
            'repeated_password': 'pass123',
            'type': 'CUSTOMER',
        }
        data.update(kwargs)
        return data

    def test_passwords_match(self):
        serializer = RegistrationSerializer(data=self.get_valid_data())
        self.assertTrue(serializer.is_valid())
        self.assertNotIn('repeated_password', serializer.errors)

    def test_passwords_do_not_match(self):
        invalid_data = self.get_valid_data(repeated_password='wrongPass')
        serializer = RegistrationSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('repeated_password', serializer.errors)

    def test_create_user_success(self):
        serializer = RegistrationSerializer(data=self.get_valid_data())
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self.assertIsInstance(user, User)
        self.assertTrue(user.check_password(self.get_valid_data()['password']))


class LoginSerializerTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tester',
            password='pass123',
            email='test@test.com',
            type='CUSTOMER'
        )

    def get_login_data(self, **kwargs):
        data = {
            'username': self.user.username,
            'password': 'pass123',
        }
        data.update(kwargs)
        return data

    def test_valid_login(self):
        serializer = LoginSerializer(data=self.get_login_data())
        serializer.is_valid(raise_exception=True)
        self.assertEqual(serializer.validated_data['user'], self.user)

    def test_invalid_login(self):
        serializer = LoginSerializer(data=self.get_login_data(password='wrongpass'))
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)