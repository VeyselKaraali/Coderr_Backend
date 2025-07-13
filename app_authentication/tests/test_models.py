from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
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

    def assert_raises_validation_error(self, user):
        with self.assertRaises(ValidationError):
            user.clean()

    def test_guest_with_email_error(self):
        user = self.create_user(is_guest=True)
        self.assert_raises_validation_error(user)

    def test_multiple_guest_with_empty_email_success(self):
        valid_test_cases = [
            {'username': 'guest1', 'email': None},
            {'username': 'guest2', 'email': None},
            {'username': 'guest3'},
            {'username': 'guest4'},
        ]

        for case in valid_test_cases:
            with self.subTest(case=case):
                user = User.objects.create_user(
                    username=case['username'],
                    email=case.get('email'),
                    password='pass123',
                    is_guest=True,
                    type='CUSTOMER'
                )
                self.assertIsNone(user.email)
                self.assertTrue(user.is_guest)

        self.assertEqual(User.objects.filter(is_guest=True).count(), len(valid_test_cases))

    def test_guest_with_superuser_error(self):
        user = self.create_user(email='', is_guest=True, is_superuser=True, type='SUPERUSER')
        self.assert_raises_validation_error(user)

    def test_superuser_wrong_type_error(self):
        user = self.create_user(is_superuser=True, type='CUSTOMER')
        self.assert_raises_validation_error(user)

    def test_superuser_correct_type_success(self):
        user = self.create_user(is_superuser=True, type='SUPERUSER')
        user.clean()

    def test_new_user_without_email_raises_error(self):
        user = self.create_user(email='', type='CUSTOMER')
        self.assert_raises_validation_error(user)

    def test_user_with_username_exists_error(self):
        User.objects.create_user(
            username='user',
            email='user1@example.com',
            password='pass123',
            type='CUSTOMER'
        )

        with self.assertRaises(ValidationError):
            User.objects.create_user(
                username='user',
                email='user2@example.com',
                password='pass123',
                type='CUSTOMER'
            )

