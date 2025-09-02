from django.contrib.auth import authenticate

from rest_framework import serializers

from app_authentication.models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'repeated_password', 'type', 'is_guest']

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({"repeated_password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('repeated_password')
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

class RegistrationGuestSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'type', 'is_guest']

    def create(self, validated_data):
        guest_number = self.get_next_guest_number()
        validated_data['username'] = f"Guest_{guest_number}"
        validated_data['email'] = f"guest_{guest_number}@example.com"

        user = CustomUser(**validated_data)
        user.set_unusable_password()
        user.save()
        return user

    @staticmethod
    def get_next_guest_number():
        last_guest = CustomUser.objects.filter(is_guest=True).order_by('-id').first()
        if last_guest:
            try:
                last_number = int(last_guest.username.split('_')[1])
            except (IndexError, ValueError):
                last_number = 0
        else:
            last_number = 0
        return last_number + 1


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        data['user'] = user
        return data