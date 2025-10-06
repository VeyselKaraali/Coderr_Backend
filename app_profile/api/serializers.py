from rest_framework import serializers
from app_profile.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.
    Provides basic user-related fields and profile information.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    type = serializers.CharField(source='user.type', read_only=True)
    is_guest = serializers.BooleanField(source='user.is_guest', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'user',
            'username',
            'first_name',
            'last_name',
            'file',
            'type',
            'is_guest',
        ]


class BusinessProfileSerializer(ProfileSerializer):
    """
    Serializer for business user profiles.
    Extends ProfileSerializer to include additional business-specific fields.
    """
    class Meta(ProfileSerializer.Meta):
        fields = ProfileSerializer.Meta.fields + [
            'location',
            'tel',
            'description',
            'working_hours',
        ]


class CustomerProfileSerializer(ProfileSerializer):
    """
    Serializer for customer user profiles.
    Currently extends ProfileSerializer without additional fields,
    but kept separate for future customization.
    """
    class Meta(ProfileSerializer.Meta):
        fields = ProfileSerializer.Meta.fields + []


class ProfileDetailSerializer(BusinessProfileSerializer):
    """
    Detailed serializer for business profiles.
    Adds read-only email field and timestamps.
    """
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta(BusinessProfileSerializer.Meta):
        fields = BusinessProfileSerializer.Meta.fields + [
            'email',       # User email address
            'created_at',  # Profile creation timestamp
            'updated_at',  # Profile last updated timestamp
        ]
