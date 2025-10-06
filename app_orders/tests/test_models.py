import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model
from app_offers.models import Offer, Detail
from app_orders.models import Order

User = get_user_model()

@pytest.mark.django_db
class TestOrderModel:

    @pytest.fixture
    def users(self):
        customer = User.objects.create(username="customer", email="customer@test.com", type="customer")
        business = User.objects.create(username="business", email="business@test.com", type="business")
        return customer, business

    @pytest.fixture
    def offer_with_detail(self, users):
        customer, business = users
        offer = Offer.objects.create(user=business, title="Test Offer", description="Desc")
        detail = Detail.objects.create(
            offer=offer,
            title="Detail 1",
            revisions=1,
            delivery_time_in_days=3,
            price=Decimal("10.00"),
            features=["feature1"],
            offer_type="basic",
        )
        return offer, detail, customer, business

    def test_create_order(self, offer_with_detail):
        offer, detail, customer, business = offer_with_detail

        order = Order.objects.create(
            customer_user=customer,
            business_user=business,
            title=detail.title,
            revisions=detail.revisions,
            delivery_time_in_days=detail.delivery_time_in_days,
            price=detail.price,
            features=detail.features,
            offer_type=detail.offer_type,
        )

        assert order.customer_user == customer
        assert order.business_user == business
        assert order.title == detail.title
        assert order.revisions == 1
        assert order.delivery_time_in_days == 3
        assert order.price == Decimal("10.00")
        assert order.features == ["feature1"]
        assert order.offer_type == "basic"
        assert order.status == "in_progress"

    def test_str_method(self, offer_with_detail):
        offer, detail, customer, business = offer_with_detail
        order = Order.objects.create(
            customer_user=customer,
            business_user=business,
            title=detail.title,
            revisions=detail.revisions,
            delivery_time_in_days=detail.delivery_time_in_days,
            price=detail.price,
            features=detail.features,
            offer_type=detail.offer_type,
        )
        assert str(order) == f"Order {order.id} - {order.title}"

    def test_status_choices(self, offer_with_detail):
        offer, detail, customer, business = offer_with_detail
        order = Order.objects.create(
            customer_user=customer,
            business_user=business,
            title=detail.title,
            revisions=detail.revisions,
            delivery_time_in_days=detail.delivery_time_in_days,
            price=detail.price,
            features=detail.features,
            offer_type=detail.offer_type,
        )
        assert order.status == "in_progress"

        for status_value, _ in Order.STATUS_CHOICES:
            order.status = status_value
            order.full_clean()

        from django.core.exceptions import ValidationError
        order.status = "invalid_status"
        with pytest.raises(ValidationError):
            order.full_clean()
