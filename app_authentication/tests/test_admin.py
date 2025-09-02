from django.contrib import admin
from django.test import TestCase

from app_authentication.models import CustomUser


class UserAdminTests(TestCase):
    def test_user_model_registered_in_admin(self):
        self.assertIn(CustomUser, admin.site._registry)

    def test_user_admin_configurations(self):
        user_admin = admin.site._registry[CustomUser]

        self.assertEqual(
            set(user_admin.readonly_fields),
            {'created_at', 'updated_at', 'last_login'}
        )

        self.assertEqual(
            user_admin.ordering,
            ['username', 'created_at']
        )

        self.assertIsNotNone(user_admin.add_fieldsets)
        self.assertIsNotNone(user_admin.fieldsets)