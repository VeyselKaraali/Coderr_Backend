from django.db.models import Min, Q
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app_authentication.permissions import IsBusinessUser, IsProfileOwnerOrReadOnly
from app_offers.models import Offer, Detail
from .pagination import CustomPagination
from .serializers import OfferSerializer, OfferCreateUpdateSerializer, OfferReadOnlySerializer, DetailSerializer


class OffersView(APIView):
    """
    API view to list all offers or create a new offer.

    - GET: List all offers with optional filtering, searching, and ordering.
    - POST: Create a new offer (only accessible by business users).
    """
    pagination_class = CustomPagination

    def get_permissions(self):
        """
        Returns permissions based on HTTP method.
        - POST: requires business user
        - GET: allows any user
        """
        if self.request.method == 'POST':
            return [IsBusinessUser()]
        return [AllowAny()]

    def get(self, request):
        """
        Handles GET requests to list offers.
        - Annotates offers with minimum price and delivery time.
        - Applies optional filters: creator_id, min_price, max_delivery_time, search.
        - Supports ordering by query parameter.
        - Paginates results using CustomPagination.
        """
        queryset = Offer.objects.all().annotate(
            min_price_annotated=Min("details__price"),
            min_delivery_time_annotated=Min("details__delivery_time_in_days"),
        )

        params = request.query_params
        if params.get("creator_id"):
            queryset = queryset.filter(user_id=params["creator_id"])
        if params.get("min_price"):
            queryset = queryset.filter(details__price__gte=params["min_price"])
        if params.get("max_delivery_time"):
            queryset = queryset.filter(details__delivery_time_in_days__lte=params["max_delivery_time"])
        if params.get("search"):
            search = params["search"]
            queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))

        ordering = params.get("ordering")
        if ordering:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by("id")

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        serializer = OfferSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """
        Handles POST requests to create a new offer.
        - Validates and saves the offer along with details.
        - Returns read-only serialized offer data.
        """
        serializer = OfferCreateUpdateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        offer = serializer.save()

        response_serializer = OfferReadOnlySerializer(offer)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class OfferView(APIView):
    """
    API view for retrieving, updating, or deleting a single offer.
    """
    def get_permissions(self):
        """
        Returns permissions based on HTTP method:
        - GET: requires authentication
        - PATCH / DELETE: requires ownership of the offer
        - Other: allows any user
        """
        if self.request.method == "GET":
            return [IsAuthenticated()]
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsAuthenticated(), IsProfileOwnerOrReadOnly()]
        return [AllowAny()]

    def get(self, request, id):
        """
        Retrieves a single offer by ID.
        - Annotates with minimum price and delivery time.
        - Returns serialized offer data.
        """
        offer = get_object_or_404(
            Offer.objects.annotate(
                min_price_annotated=Min("details__price"),
                min_delivery_time_annotated=Min("details__delivery_time_in_days"),
            ),
            pk=id
        )
        serializer = OfferSerializer(offer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        """
        Updates an existing offer.
        - Partial updates supported.
        - Validates and saves updated offer and its details.
        - Returns read-only serialized offer data.
        """
        offer = get_object_or_404(Offer, pk=id)
        self.check_object_permissions(request, offer)

        serializer = OfferCreateUpdateSerializer(offer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_serializer = OfferReadOnlySerializer(offer)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        """
        Deletes an offer.
        - Requires ownership permission.
        - Returns HTTP 204 No Content on success.
        """
        offer = get_object_or_404(Offer, pk=id)
        self.check_object_permissions(request, offer)
        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OfferDetailView(APIView):
    """
    API view to retrieve a single detail object.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        """
        Retrieves a single detail by ID.
        - Returns serialized detail data.
        """
        detail = get_object_or_404(Detail, pk=id)
        serializer = DetailSerializer(detail)
        return Response(serializer.data, status=status.HTTP_200_OK)
