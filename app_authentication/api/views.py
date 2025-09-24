from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from app_profile.models import Profile
from .serializers import LoginSerializer, RegistrationSerializer, RegistrationGuestSerializer


class RegistrationView(APIView):
    def post(self, request):
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
    throttle_classes = [AnonRateThrottle]
    throttle_scope = 'login'

    def post(self, request):
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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_205_RESET_CONTENT)