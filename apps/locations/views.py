from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.utils import timezone
from django.utils.dateparse import parse_date

from .models import Location
from .selectors import (
    get_active_location_by_slug,
    list_active_locations,
    search_locations,
    get_available_times_by_location
)
from .serializers import LocationSerializer, LocationSuggestionSerializer


class LocationListView(APIView):
    """Активные точки и свободные часы на сегодня."""

    def get(self, request):
        location_type = request.query_params.get("type")
        query = request.query_params.get("q", "").strip()

        allowed_types = {
            Location.LocationType.SELF_SERVICE,
            Location.LocationType.STAFF_SERVICE,
            Location.LocationType.BOTH,
        }

        date_value = request.query_params.get("date")

        if date_value:
            selected_date = parse_date(date_value)
            if selected_date is None:
                return Response(
                    {"date": "Укажите дату в формате YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            selected_date = timezone.localdate()

        if location_type and location_type not in allowed_types:
            return Response(
                {
                    "type": (
                        "Допустимые значения: self_service, "
                        "staff_service или both."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        locations = list(list_active_locations(
            location_type=location_type,
            query=query,
        ))
        available_times = get_available_times_by_location(locations, selected_date)

        serializer = LocationSerializer(
            locations,
            many=True,
            context={"available_times": available_times},
        )
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

        return Response(LocationSerializer(location).data)


class LocationSearchView(APIView):
    """Подсказки существующих активных точек по адресу."""

    def get(self, request):
        query = request.query_params.get("q", "").strip()

        if len(query) < 2:
            return Response(
                {"q": "Введите адрес хотя бы из 2 символов."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        locations = search_locations(query)
        serializer = LocationSuggestionSerializer(locations, many=True)
        return Response(serializer.data)