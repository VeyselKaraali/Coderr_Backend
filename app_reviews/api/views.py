from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from app_authentication.permissions import IsReviewerOrReadOnly
from app_reviews.api.serializers import ReviewSerializer, ReviewCreateUpdateSerializer
from app_reviews.models import Review


class ReviewView(APIView):
    def get_permissions(self):
        if self.request.method in ["GET", "POST"]:
            return [IsAuthenticated()]
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsAuthenticated(), IsReviewerOrReadOnly()]
        return [AllowAny()]

    def get(self, request):
        queryset = Review.objects.all()

        business_user_id = request.query_params.get("business_user_id")
        if business_user_id:
            queryset = queryset.filter(business_user_id=business_user_id)

        reviewer_id = request.query_params.get("reviewer_id")
        if reviewer_id:
            queryset = queryset.filter(reviewer_id=reviewer_id)

        ordering = request.query_params.get("ordering")
        if ordering in ["updated_at", "rating"]:
            queryset = queryset.order_by(ordering)

        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ReviewCreateUpdateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            review = serializer.save()
            response_serializer = ReviewSerializer(review)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        review = get_object_or_404(Review, pk=id)

        serializer = ReviewCreateUpdateSerializer(
            review,
            data=request.data,
            partial=True,
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            response_serializer = ReviewSerializer(review)
            return Response(response_serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        review = get_object_or_404(Review, pk=id)
        self.check_object_permissions(request, review)

        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
