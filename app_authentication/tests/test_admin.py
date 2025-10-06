import pytest
from django.contrib.admin.sites import AdminSite
from app_authentication.admin import UserAdmin
from app_authentication.models import CustomUser

@pytest.mark.django_db
class TestUserAdmin:

    @pytest.fixture
    def admin_user(self, db):
        return CustomUser.objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="AdminPass123!"
        )

    @pytest.fixture
    def normal_user(self, db):
        return CustomUser.objects.create_user(
            username="user",
            email="user@test.com",
            password="Password123!",
            type="customer"
        )

    @pytest.fixture
    def admin_site(self):
        return AdminSite()

    def test_list_display_fields(self, admin_site):
        model_admin = UserAdmin(CustomUser, admin_site)
        expected = ['id', 'username', 'is_active', 'is_staff', 'is_superuser']
        assert model_admin.list_display == expected

    def test_readonly_fields(self, admin_site):
        model_admin = UserAdmin(CustomUser, admin_site)
        expected = ['last_login', 'is_staff', 'is_superuser', 'created_at', 'updated_at']
        assert model_admin.readonly_fields == expected

    def test_get_readonly_fields_on_edit(self, admin_site, normal_user):
        model_admin = UserAdmin(CustomUser, admin_site)
        readonly = model_admin.get_readonly_fields(None, normal_user)
        expected = ['last_login', 'is_staff', 'is_superuser', 'created_at', 'updated_at']
        assert readonly == expected

    def test_get_readonly_fields_on_add(self, admin_site):
        model_admin = UserAdmin(CustomUser, admin_site)
        readonly = model_admin.get_readonly_fields(None, None)
        expected = ['last_login', 'is_staff', 'is_superuser', 'created_at', 'updated_at']
        assert readonly == expected

    def test_fieldsets_on_add(self, admin_site):
        model_admin = UserAdmin(CustomUser, admin_site)
        fieldsets = model_admin.get_fieldsets(None)
        assert any('Create New User' in str(fs) for fs in model_admin.add_fieldsets)

    def test_fieldsets_on_edit(self, admin_site, normal_user):
        model_admin = UserAdmin(CustomUser, admin_site)
        fieldsets = model_admin.get_fieldsets(None, normal_user)
        labels = [fs[0] for fs in fieldsets]
        assert 'Login Information' in labels
        assert 'Permissions' in labels
        assert 'Activity' in labels