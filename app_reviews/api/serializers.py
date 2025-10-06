from rest_framework import serializers
from app_reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.
    Used for reading/displaying review data.

    read_only_fields: Fields that should not be editable by clients.
    """
    read_only_fields = ["id", "reviewer", "created_at", "updated_at"]

    class Meta:
        model = Review
        fields = [
            "id",  # Review ID
            "business_user",  # Business user being reviewed
            "reviewer",  # User who submitted the review
            "rating",  # Numeric rating
            "description",  # Review text
            "created_at",  # Timestamp when the review was created
            "updated_at",  # Timestamp when the review was last updated
        ]


class ReviewCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating reviews.
    Includes validation to prevent self-reviews and duplicate reviews.
    """

    class Meta:
        model = Review
        fields = ["business_user", "rating", "description"]

    def validate(self, data):
        """
        Custom validation:
        - Prevents a user from reviewing themselves.
        - Prevents a user from reviewing the same business more than once.
        """
        request = self.context.get("request")
        reviewer = request.user
        business_user = data.get("business_user")

        if reviewer == business_user:
            raise serializers.ValidationError("You cannot review yourself.")

        if Review.objects.filter(business_user=business_user, reviewer=reviewer).exists():
            raise serializers.ValidationError("You have already reviewed this provider.")

        return data

    def create(self, validated_data):
        """
        Assigns the current authenticated user as the reviewer when creating a review.
        """
        request = self.context.get("request")
        validated_data["reviewer"] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Updates the rating and description of an existing review.
        """
        instance.rating = validated_data.get("rating", instance.rating)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        return instance
