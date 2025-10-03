from django.db.models import Q
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from app_authentication.models import CustomUser
from app_authentication.permissions import IsCustomerUser, IsBusinessUser
from app_offers.models import Detail
from app_orders.api.serializers import OrderSerializer, OrderCreateSerializer
from app_orders.models import Order


class OrdersView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        if self.request.method == "POST":
            return [IsAuthenticated(), IsCustomerUser()]
        return [AllowAny()]

    def get(self, request):
        user = request.user
        queryset = Order.objects.filter(Q(customer_user=user) | Q(business_user=user))
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        offer_detail_id = serializer.validated_data["offer_detail_id"]
        offer_detail = get_object_or_404(Detail, pk=offer_detail_id)


        order = Order.objects.create(
            customer_user=request.user,
            business_user=offer_detail.offer.user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            status="in_progress",
        )

        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class OrderView(APIView):
    def get_permissions(self):
        if self.request.method == "PATCH":
            return [IsAuthenticated(), IsBusinessUser()]
        if self.request.method == "DELETE":
            return [IsAuthenticated(), IsAdminUser()]
        return [AllowAny()]

    def patch(self, request, id):
        order = get_object_or_404(Order, pk=id)

        status_value = request.data.get("status")
        if status_value not in dict(Order.STATUS_CHOICES):
            return Response(
                {"detail": "Invalid status value."},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = status_value
        order.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        order = get_object_or_404(Order, pk=id)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        business_user = get_object_or_404(CustomUser, pk=business_user_id, type='business')
        order_count = Order.objects.filter(business_user=business_user, status='in_progress').count()
        return Response({'order_count': order_count}, status=200)


class CompletedOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        business_user = get_object_or_404(CustomUser, pk=business_user_id, type='business')
        completed_order_count = Order.objects.filter(business_user=business_user, status='completed').count()
        return Response({'completed_order_count': completed_order_count}, status=200)