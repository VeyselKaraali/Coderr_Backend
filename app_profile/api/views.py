from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app_authentication.models import CustomUser
from app_authentication.permissions import IsProfileOwnerOrReadOnly
from app_profile.api.serializers import BusinessProfileSerializer, CustomerProfileSerializer, ProfileDetailSerializer
from app_profile.models import Profile


class ProfileDetailView(APIView):
    permission_classes = [IsAuthenticated, IsProfileOwnerOrReadOnly]

    def get(self, request, id):
        profile = get_object_or_404(Profile, pk=id)
        serializer = ProfileDetailSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        profile = get_object_or_404(Profile, pk=id)

        data = request.data.copy()

        for field in ['first_name', 'last_name', 'location', 'tel', 'description', 'working_hours']:
            if field not in data or data[field] is None:
                data[field] = ''


        serializer = ProfileDetailSerializer(profile, data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        new_email = data.get('email')
        if new_email and CustomUser.objects.filter(email=new_email).exclude(pk=profile.user.pk).exists():
            raise ValidationError({"email": "This email is already in use."})

        serializer.save()

        if new_email:
            profile.user.email = new_email
            profile.user.save()

        return Response(ProfileDetailSerializer(profile).data, status=status.HTTP_200_OK)


class ProfileBusinessView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        business_profiles = Profile.objects.filter(user__type='business')
        serializer = BusinessProfileSerializer(business_profiles, many=True)
        return Response(serializer.data)


class ProfileCustomerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        business_profiles = Profile.objects.filter(user__type='customer')
        serializer = CustomerProfileSerializer(business_profiles, many=True)
        return Response(serializer.data)
