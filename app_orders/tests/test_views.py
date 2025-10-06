import pytest
from rest_framework.test import APIClient
from django.urls import reverse

from app_authentication.models import CustomUser
from app_offers.models import Offer, Detail
from app_orders.models import Order

@pytest.mark.django_db
class TestOrdersViews:

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
            title="Basic",
            revisions=1,
            delivery_time_in_days=5,
            price=100.0,
            features=[],
            offer_type="basic"
        )
        return offer

    @pytest.fixture
    def client_customer(self, customer):
        client = APIClient()
        client.force_authenticate(user=customer)
        return client

    @pytest.fixture
    def client_business(self, business):
        client = APIClient()
        client.force_authenticate(user=business)
        return client

    def test_get_orders_empty(self, client_customer):
        url = reverse('orders')
        response = client_customer.get(url)
        assert response.status_code == 200
        assert response.data == []

    def test_post_order_creates_order(self, client_customer, offer):
        url = reverse('orders')
        detail = offer.details.first()
        response = client_customer.post(url, {"offer_detail_id": detail.id}, format='json')
        assert response.status_code == 201
        data = response.data
        assert data['title'] == detail.title
        assert data['customer_user'] == detail.offer.user.id or data['customer_user'] == client_customer.handler._force_user.id
        assert data['business_user'] == offer.user.id

    def test_patch_order_status(self, client_business, offer, customer):
        detail = offer.details.first()
        order = Order.objects.create(
            customer_user=customer,
            business_user=offer.user,
            title=detail.title,
            revisions=detail.revisions,
            delivery_time_in_days=detail.delivery_time_in_days,
            price=detail.price,
            features=detail.features,
            offer_type=detail.offer_type,
            status='in_progress'
        )
        url = reverse('order', args=[order.id])
        response = client_business.patch(url, {"status": "completed"}, format='json')
        assert response.status_code == 200
        assert response.data['status'] == 'completed'

    def test_delete_order_as_admin(self, client_business, offer, customer, db, django_user_model):
        admin_user = django_user_model.objects.create_superuser(username='admin', email='admin@test.com', password='pass')
        client = APIClient()
        client.force_authenticate(admin_user)
        detail = offer.details.first()
        order = Order.objects.create(
            customer_user=customer,
            business_user=offer.user,
            title=detail.title,
            revisions=detail.revisions,
            delivery_time_in_days=detail.delivery_time_in_days,
            price=detail.price,
            features=detail.features,
            offer_type=detail.offer_type,
            status='in_progress'
        )
        url = reverse('order', args=[order.id])
        response = client.delete(url)
        assert response.status_code == 204
        assert Order.objects.filter(id=order.id).count() == 0

    def test_order_count_views(self, client_business, offer, customer):
        detail = offer.details.first()
        Order.objects.create(
            customer_user=customer,
            business_user=offer.user,
            title=detail.title,
            revisions=detail.revisions,
            delivery_time_in_days=detail.delivery_time_in_days,
            price=detail.price,
            features=detail.features,
            offer_type=detail.offer_type,
            status='in_progress'
        )
        url = reverse('order_count_view', args=[offer.user.id])
        response = client_business.get(url)
        assert response.status_code == 200
        assert response.data['order_count'] == 1

        order = Order.objects.create(
            customer_user=customer,
            business_user=offer.user,
            title=detail.title,
            revisions=detail.revisions,
            delivery_time_in_days=detail.delivery_time_in_days,
            price=detail.price,
            features=detail.features,
            offer_type=detail.offer_type,
            status='completed'
        )
        url_completed = reverse('completed_order_view', args=[offer.user.id])
        response_completed = client_business.get(url_completed)
        assert response_completed.status_code == 200
        assert response_completed.data['completed_order_count'] == 1