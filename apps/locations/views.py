from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Location
from .selectors import get_active_location_by_slug, list_active_locations
from .serializers import LocationSerializer


class LocationListView(APIView):
    """Список активных точек для карты."""

    def get(self, request):
        location_type = request.query_params.get("type")
        query = request.query_params.get("q")

        allowed_types = {
            Location.LocationType.SELF_SERVICE,
            Location.LocationType.STAFF_SERVICE,
        }

        if location_type and location_type not in allowed_types:
            return Response(
                {
                    "type": (
                        "Допустимые значения: "
                        "self_service или staff_service."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        locations = list_active_locations(
            location_type=location_type,
            query=query,
        )
        serializer = LocationSerializer(locations, many=True)

        return Response(serializer.data)


class LocationDetailView(APIView):
    """Подробности активной точки."""

    def get(self, request, slug):
        location = get_active_location_by_slug(slug)

        if location is None:
            return Response(
                {"detail": "Точка не найдена."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = LocationSerializer(location)
        return Response(serializer.data)