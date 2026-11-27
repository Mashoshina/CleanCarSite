from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .selectors import list_reviews
from .serializers import ReviewSerializer


class ReviewListView(APIView):
    """Публичный список отзывов. При limit можно получить только часть."""

    permission_classes = [AllowAny]

    def get(self, request):
        limit_value = request.query_params.get("limit")
        limit = None

        if limit_value is not None:
            try:
                limit = int(limit_value)
            except ValueError:
                return Response(
                    {"limit": "Укажите целое положительное число."},
                    status=400,
                )

            if limit < 1:
                return Response(
                    {"limit": "Укажите целое положительное число."},
                    status=400,
                )    

        reviews = list_reviews(limit=limit)
        return Response(ReviewSerializer(reviews, many=True).data)
    
    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = serializer.save()

        return Response(
            ReviewSerializer(review).data,
            status=status.HTTP_201_CREATED,
        )