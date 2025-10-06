import pytest
from django.db import IntegrityError
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
        description="Excellent service!"
    )

class TestReviewModel:

    def test_review_creation(self, review, users):
        reviewer, business = users
        assert review.reviewer == reviewer
        assert review.business_user == business
        assert review.rating == 5
        assert review.description == "Excellent service!"
        assert review.id is not None

    def test_review_str(self, review):
        expected_str = f"Review {review.id} by {review.reviewer} for {review.business_user} ({review.rating})"
        assert str(review) == expected_str

    def test_unique_constraint(self, review, users):
        reviewer, business = users
        with pytest.raises(IntegrityError):
            Review.objects.create(
                reviewer=reviewer,
                business_user=business,
                rating=4,
                description="Duplicate review"
            )

    def test_rating_choices(self, review):
        assert 1 <= review.rating <= 5
