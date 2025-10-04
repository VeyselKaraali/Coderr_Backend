from rest_framework import serializers
from app_reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    read_only_fields = ["id", "reviewer", "created_at", "updated_at"]

    class Meta:
        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]


class ReviewCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["business_user", "rating", "description"]

    def validate(self, data):
        request = self.context.get("request")
        reviewer = request.user
        business_user = data.get("business_user")

        if reviewer == business_user:
            raise serializers.ValidationError("You cannot review yourself.")

        if Review.objects.filter(business_user=business_user, reviewer=reviewer).exists():
            raise serializers.ValidationError("You have already reviewed this provider.")

        return data

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["reviewer"] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.rating = validated_data.get("rating", instance.rating)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        return instance
