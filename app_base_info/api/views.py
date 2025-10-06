from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Count

from app_reviews.models import Review
from app_authentication.models import CustomUser
from app_offers.models import Offer


class BaseInfoView(APIView):
    """
    API view to provide basic statistics about the platform.

    Returns:
        - Total number of reviews
        - Average review rating
        - Total number of business profiles
        - Total number of offers
    """

    def get(self, request):
        """
        Handles GET requests to fetch platform statistics.

        Aggregates review statistics (count and average rating),
        counts business users, and counts total offers.

        Returns:
            Response: JSON containing review_count, average_rating,
                      business_profile_count, and offer_count.
            Status: 200 OK on success, 500 Internal Server Error on failure.
        """
        try:
            review_stats = Review.objects.aggregate(review_count=Count('id'), average_rating=Avg('rating'))
            average_rating = review_stats["average_rating"]
            average_rating = float(average_rating) if average_rating is not None else 0.0

            data = {
                "review_count": review_stats["review_count"] or 0,
                "average_rating": round(average_rating, 1),
                "business_profile_count": CustomUser.objects.filter(type='business').count(),
                "offer_count": Offer.objects.count()
            }

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            """
            Handles unexpected exceptions and returns error details.
            """
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
