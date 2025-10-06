from django.db import models
from django.conf import settings


class Review(models.Model):
    """
    Model representing a review given by a user (reviewer) to a business user.

    Fields:
        - business_user: Foreign key to the user being reviewed (business).
        - reviewer: Foreign key to the user who wrote the review.
        - rating: Integer rating from 1 to 5.
        - description: Optional text describing the review.
        - created_at: Timestamp when the review was created.
        - updated_at: Timestamp when the review was last updated.

    Meta:
        - ordering: Default ordering by most recently updated reviews first.
        - unique_together: Ensures a reviewer can only review the same business once.
    """
    business_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_reviews")
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="written_reviews")
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        unique_together = ("business_user", "reviewer")

    def __str__(self):
        """
        Returns a human-readable string representation of the review,
        showing the review ID, reviewer, business user, and rating.
        """
        return f"Review {self.id} by {self.reviewer} for {self.business_user} ({self.rating})"
