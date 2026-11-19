from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Location
from .selectors import get_active_location_by_slug, list_active_locations
from .serializers import LocationSerializer

from .selectors import search_locations
from .serializers import LocationSuggestionSerializer

from django.shortcuts import render


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
    

class LocationSearchView(APIView):
    """Подсказки существующих активных точек по адресу."""

    def get(self, request):
        query = request.query_params.get("q", "").strip()

        if len(query) < 2:
            return Response(
                {"q": "Введите адресс хотя бы из 2 символов."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        locations = search_locations(query)
        serializer = LocationSuggestionSerializer(locations, many=True)

        return Response(serializer.data)
    
def locations_page(request):
    locations = list_active_locations()

    return render(
        request,
        "locations.html",
        {"locations": locations},
    )