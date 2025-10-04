from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Count

from app_reviews.models import Review
from app_authentication.models import CustomUser
from app_offers.models import Offer


class BaseInfoView(APIView):
    def get(self, request):
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
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
