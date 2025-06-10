from rest_framework import serializers
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from app_authentication.api.serializers import RegistrationSerializer, LoginSerializer

User = get_user_model()

class RegistrationSerializerTests(APITestCase):
    def get_valid_data(self, **kwargs):
        data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'pass123',
            'password_repeat': 'pass123',
            'type': 'CUSTOMER',
        }
        data.update(kwargs)
        return data

    def test_passwords_match(self):
        serializer = RegistrationSerializer(data=self.get_valid_data())
        self.assertTrue(serializer.is_valid())
        self.assertNotIn('password_repeat', serializer.errors)

    def test_passwords_do_not_match(self):
        invalid_data = self.get_valid_data(password_repeat='wrongPass')
        serializer = RegistrationSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password_repeat', serializer.errors)

    def test_create_user_success(self):
        serializer = RegistrationSerializer(data=self.get_valid_data())
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self.assertIsInstance(user, User)
        self.assertTrue(user.check_password(self.get_valid_data()['password']))