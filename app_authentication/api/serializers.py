from django.contrib.auth import authenticate
from rest_framework import serializers
from app_authentication.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_repeat', 'type']

    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    def validate(self, data):
        if data.get('password') != data.get('password_repeat'):
            raise serializers.ValidationError({"password_repeat": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password_repeat')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        data['user'] = user
        return data
