import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from app_reviews.models import Review
from app_authentication.models import CustomUser as User

@pytest.fixture
def users(db):
    reviewer = User.objects.create_user(username="reviewer", email="reviewer@test.com", password="testpass123", type="customer")
    business = User.objects.create_user(username="business", email="business@test.com", password="testpass123", type="business")
    return reviewer, business

@pytest.fixture
def client_reviewer(users):
    reviewer, _ = users
    client = APIClient()
    client.force_authenticate(user=reviewer)
    return client

@pytest.fixture
def review(users):
    reviewer, business = users
    return Review.objects.create(
        business_user=business,
        reviewer=reviewer,
        rating=4,
        description="Great service"
    )

@pytest.mark.django_db
class TestReviewViews:

    def test_get_reviews(self, client_reviewer, review):
        url = reverse("reviews")
        response = client_reviewer.get(url)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["rating"] == review.rating
        assert data[0]["description"] == review.description

    def test_post_review_creates_review(self, client_reviewer, users):
        _, business = users
        url = reverse("reviews")
        response = client_reviewer.post(url, {"business_user": business.id, "rating": 5, "description": "Excellent"}, format="json")
        assert response.status_code == 201
        data = response.json()
        assert data["rating"] == 5
        assert data["description"] == "Excellent"
        assert data["reviewer"] == client_reviewer.handler._force_user.id

    def test_post_review_self_review_fails(self, client_reviewer, users):
        reviewer, _ = users
        url = reverse("reviews")
        response = client_reviewer.post(url, {"business_user": reviewer.id, "rating": 5, "description": "Self review"}, format="json")
        assert response.status_code == 400
        assert "You cannot review yourself." in str(response.json())

    def test_patch_review_updates_review(self, client_reviewer, review):
        url = reverse("review", args=[review.id])
        response = client_reviewer.patch(url, {"rating": 3, "description": "Updated"}, format="json")
        assert response.status_code == 200
        review.refresh_from_db()
        assert review.rating == 3
        assert review.description == "Updated"

    def test_delete_review(self, client_reviewer, review):
        url = reverse("review", args=[review.id])
        response = client_reviewer.delete(url)
        assert response.status_code == 204
        assert Review.objects.filter(id=review.id).count() == 0

    def test_filter_reviews_by_business_user(self, client_reviewer, review, users):
        _, business = users
        url = reverse("reviews") + f"?business_user_id={business.id}"
        response = client_reviewer.get(url)
        data = response.json()
        assert len(data) == 1
        assert data[0]["business_user"] == business.id

    def test_filter_reviews_by_reviewer(self, client_reviewer, review, users):
        reviewer, _ = users
        url = reverse("reviews") + f"?reviewer_id={reviewer.id}"
        response = client_reviewer.get(url)
        data = response.json()
        assert len(data) == 1
        assert data[0]["reviewer"] == reviewer.id
