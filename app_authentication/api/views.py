from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from app_profile.models import Profile
from .serializers import LoginSerializer, RegistrationSerializer, RegistrationGuestSerializer


class RegistrationView(APIView):
    """
    API view for user registration.

    Supports both regular and guest user registration.
    Creates a Profile for the user and returns an auth token upon successful registration.
    """
    def post(self, request):
        """
        Handles POST requests to register a user.
        - Determines if the user is a guest.
        - Validates and saves the user using the appropriate serializer.
        - Creates a Profile for the user if it does not exist.
        - Generates an authentication token.
        - Returns user details and token in the response.
        """
        is_guest = str(request.data.get("is_guest", "false")).lower() == "true"

        if is_guest:
            serializer = RegistrationGuestSerializer(data=request.data)
        else:
            serializer = RegistrationSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        Profile.objects.get_or_create(user=user)

        token, created = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'username': user.username,
            'email': user.email,
            'user_id': user.id,
            'is_guest': user.is_guest
        }
        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    API view for user login.

    - Uses throttling to prevent abuse of login endpoint.
    - Returns authentication token and user information upon successful login.
    """
    throttle_classes = [AnonRateThrottle]
    throttle_scope = 'login'

    def post(self, request):
        """
        Handles POST requests to log in a user.
        - Validates login credentials via LoginSerializer.
        - Generates or retrieves an authentication token.
        - Returns user details and token in the response.
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'username': user.username,
            'email': user.email,
            'user_id': user.id,
            'is_guest': user.is_guest
        }
        return Response(data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    API view for user logout.

    - Requires authentication.
    - Deletes the user's authentication token, effectively logging them out.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handles POST requests to log out a user.
        - Deletes the user's auth token.
        - Returns HTTP 205 Reset Content on success.
        """
        request.user.auth_token.delete()
        return Response(status=status.HTTP_205_RESET_CONTENT)
