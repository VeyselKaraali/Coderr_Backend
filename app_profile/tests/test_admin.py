import pytest
from app_profile.admin import ProfileAdmin
from app_profile.models import Profile
from app_authentication.models import CustomUser
from django.contrib.admin.sites import AdminSite

@pytest.mark.django_db
class TestProfileAdmin:

    @pytest.fixture
    def site(self):
        return AdminSite()

    @pytest.fixture
    def user(self):
        return CustomUser.objects.create_user(
            username="user",
            email="user@test.com",
            password="password123",
            type="business"
        )

    @pytest.fixture
    def profile(self, user):
        return Profile.objects.create(user=user, first_name="Alice", last_name="Smith")

    @pytest.fixture
    def admin(self, site):
        return ProfileAdmin(Profile, site)

    def test_list_display(self, admin):
        expected_fields = [
            'id', 'username', 'email', 'user_type', 'first_name', 'last_name',
            'file', 'location', 'tel', 'description', 'working_hours',
            'created_at', 'updated_at'
        ]
        assert admin.list_display == expected_fields

    def test_search_fields(self, admin):
        assert admin.search_fields == ['user__username', 'user__email', 'first_name', 'last_name']

    def test_ordering(self, admin):
        assert admin.ordering == ['user__username']

    def test_get_readonly_fields_when_editing(self, admin, profile):
        readonly_fields = admin.get_readonly_fields(None, profile)
        expected = ('id', 'username', 'email', 'user_type', 'created_at', 'updated_at')
        assert readonly_fields == expected

    def test_get_readonly_fields_when_creating(self, admin):
        readonly_fields = admin.get_readonly_fields(None, None)
        assert readonly_fields == ()

    def test_get_fieldsets_when_editing(self, admin, profile):
        fieldsets = admin.get_fieldsets(None, profile)
        assert len(fieldsets) == 3
        assert fieldsets[0][0] == 'User Info'
        assert 'id' in fieldsets[0][1]['fields']
        assert 'username' in fieldsets[0][1]['fields']

    def test_get_fieldsets_when_creating(self, admin):
        fieldsets = admin.get_fieldsets(None, None)
        assert len(fieldsets) == 2
        assert fieldsets[0][0] == 'User Info'
