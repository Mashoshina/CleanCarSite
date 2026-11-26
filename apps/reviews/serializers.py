from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("id", "name", "rating", "comment")

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Имя автора отзыва обязательно.")
        return value

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Рейтинг должен быть от 1 до 5.")
        return value