import pytest
from app_orders.api.serializers import OrderSerializer, OrderCreateSerializer
from app_orders.models import Order
from app_offers.models import Offer, Detail
from app_authentication.models import CustomUser


@pytest.mark.django_db
class TestOrderSerializers:

    @pytest.fixture
    def customer(self):
        return CustomUser.objects.create(username="customer", email="customer@test.com", type="customer")

    @pytest.fixture
    def business(self):
        return CustomUser.objects.create(username="business", email="business@test.com", type="business")

    @pytest.fixture
    def offer(self, business):
        offer = Offer.objects.create(user=business, title="Test Offer", description="Desc")
        Detail.objects.create(
            offer=offer,
            title="Detail 1",
            revisions=2,
            delivery_time_in_days=3,
            price=100,
            features=[],
            offer_type="basic"
        )
        return offer

    @pytest.fixture
    def order(self, customer, offer):
        detail = offer.details.first()
        return Order.objects.create(
            customer_user=customer,
            business_user=offer.user,
            title=detail.title,
            revisions=detail.revisions,
            delivery_time_in_days=detail.delivery_time_in_days,
            price=detail.price,
            features=detail.features,
            offer_type=detail.offer_type,
            status="in_progress",
        )

    def test_order_serializer_fields(self, order):
        serializer = OrderSerializer(order)
        data = serializer.data

        assert data["id"] == order.id
        assert data["customer_user"] == order.customer_user.id
        assert data["business_user"] == order.business_user.id
        assert data["title"] == order.title
        assert data["revisions"] == order.revisions
        assert data["delivery_time_in_days"] == order.delivery_time_in_days
        assert float(data["price"]) == float(order.price)
        assert data["features"] == order.features
        assert data["offer_type"] == order.offer_type
        assert data["status"] == order.status

    def test_order_create_serializer_valid(self, offer, customer):
        detail = offer.details.first()
        serializer = OrderCreateSerializer(data={"offer_detail_id": detail.id})
        assert serializer.is_valid(), serializer.errors

    def test_order_create_serializer_invalid(self):
        serializer = OrderCreateSerializer(data={"offer_detail_id": 999})
        assert not serializer.is_valid()
        assert "offer_detail_id" in serializer.errors or serializer.errors != {}
