import pytest
from rest_framework.exceptions import ValidationError
from app_reviews.api.serializers import ReviewSerializer, ReviewCreateUpdateSerializer
from app_reviews.models import Review
from app_authentication.models import CustomUser as User

@pytest.fixture
def users(db):
    reviewer = User.objects.create_user(
        username="reviewer",
        email="reviewer@test.com",
        password="testpass123",
        type="customer"
    )
    business = User.objects.create_user(
        username="business",
        email="business@test.com",
        password="testpass123",
        type="business"
    )
    return reviewer, business

@pytest.fixture
def review(db, users):
    reviewer, business = users
    return Review.objects.create(
        reviewer=reviewer,
        business_user=business,
        rating=5,
        description="Great service!"
    )

class TestReviewSerializers:

    def test_review_serializer_fields(self, review):
        serializer = ReviewSerializer(review)
        data = serializer.data

        assert data["id"] == review.id
        assert data["reviewer"] == review.reviewer.id
        assert data["business_user"] == review.business_user.id
        assert data["rating"] == review.rating
        assert data["description"] == review.description
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_update_serializer_valid(self, users):
        reviewer, business = users
        data = {"business_user": business.id, "rating": 4, "description": "Good work!"}
        serializer = ReviewCreateUpdateSerializer(data=data, context={"request": type("Request", (), {"user": reviewer})()})
        assert serializer.is_valid(), serializer.errors
        review = serializer.save()
        assert review.reviewer == reviewer
        assert review.business_user == business
        assert review.rating == 4
        assert review.description == "Good work!"

    def test_create_update_serializer_self_review_invalid(self, users):
        reviewer, _ = users
        data = {"business_user": reviewer.id, "rating": 5, "description": "Self review"}
        serializer = ReviewCreateUpdateSerializer(data=data, context={"request": type("Request", (), {"user": reviewer})()})
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_create_update_serializer_duplicate_review_invalid(self, review, users):
        reviewer, business = users
        data = {"business_user": business.id, "rating": 5, "description": "Duplicate"}
        serializer = ReviewCreateUpdateSerializer(data=data, context={"request": type("Request", (), {"user": reviewer})()})
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)
