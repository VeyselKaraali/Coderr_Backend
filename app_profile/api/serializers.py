from rest_framework import serializers

from app_profile.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
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
    class Meta(ProfileSerializer.Meta):
        fields = ProfileSerializer.Meta.fields + [
            'location',
            'tel',
            'description',
            'working_hours',
        ]


class CustomerProfileSerializer(ProfileSerializer):
    class Meta(ProfileSerializer.Meta):
        fields = ProfileSerializer.Meta.fields + [

        ]


class ProfileDetailSerializer(BusinessProfileSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta(BusinessProfileSerializer.Meta):
        fields = BusinessProfileSerializer.Meta.fields + [
            'email',
            'created_at',
            'updated_at',
        ]
