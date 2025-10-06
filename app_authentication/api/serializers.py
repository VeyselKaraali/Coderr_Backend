from django.contrib.auth import authenticate
from rest_framework import serializers
from app_authentication.models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Fields:
        - username: The username of the user.
        - email: The email address of the user.
        - password: The user's password (write-only).
        - repeated_password: Password confirmation (write-only).
        - type: Type of the user.
        - is_guest: Boolean indicating if the user is a guest.
    """
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'repeated_password', 'type', 'is_guest']

    def validate(self, data):
        """
        Validates that the password and repeated_password match.
        Raises a ValidationError if they do not.
        """
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({"repeated_password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        """
        Creates a new user after validation.
        - Removes 'repeated_password' from validated data.
        - Sets the user's password properly (hashed).
        - Saves the user to the database.
        """
        validated_data.pop('repeated_password')
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class RegistrationGuestSerializer(serializers.ModelSerializer):
    """
    Serializer for guest user registration.

    Fields:
        - username: Auto-generated guest username (read-only).
        - email: Auto-generated guest email (read-only).
        - type: User type.
        - is_guest: Boolean indicating the user is a guest.
    """
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'type', 'is_guest']

    def create(self, validated_data):
        """
        Creates a new guest user.
        - Generates sequential guest numbers for username and email.
        - Sets an unusable password as login is not required.
        - Saves the guest user to the database.
        """
        guest_number = self.get_next_guest_number()
        validated_data['username'] = f"Guest_{guest_number}"
        validated_data['email'] = f"guest_{guest_number}@example.com"

        user = CustomUser(**validated_data)
        user.set_unusable_password()
        user.save()
        return user

    @staticmethod
    def get_next_guest_number():
        """
        Determines the next guest number by checking the last guest in the database.
        - If no guests exist, starts at 1.
        - If extraction of the last number fails, defaults to 0.
        """
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
    """
    Serializer for user login.

    Fields:
        - username: The username of the user.
        - password: The password of the user (write-only).
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validates login credentials.
        - Authenticates the user using username and password.
        - Raises a ValidationError if credentials are invalid.
        - Returns the authenticated user in validated data.
        """
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        data['user'] = user
        return data
