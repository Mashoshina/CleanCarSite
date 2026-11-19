from django.db.models import Q

from .models import Location

def location_supports_booking_type(location, booking_type):
    """Проверить, поддерживает ли точка указанный формат брони."""
    supported_types = {
        Location.LocationType.SELF_SERVICE: {
            Location.LocationType.SELF_SERVICE,
        },
        Location.LocationType.STAFF_SERVICE: {
            Location.LocationType.STAFF_SERVICE,
        },
        Location.LocationType.BOTH: {
            Location.LocationType.SELF_SERVICE,
            Location.LocationType.STAFF_SERVICE,
        },
    }

    return booking_type in supported_types.get(location.location_type, set())

def search_locations(query, limit=10):
    """Найти активные точки по части адреса для подсказок."""
    query = (query or "").strip()

    # Не искать по пустому или слишком короткому запросу.
    if len(query) < 2:
        return Location.objects.none()

    return Location.objects.filter(
        is_active=True,
        address__icontains=query,
    ).order_by("address")[:limit]

def list_active_locations(location_type=None):
    """Вернуть активные точки, с необязательной фильтрацией по типу и адресу."""
    locations = Location.objects.filter(is_active=True)

    if location_type == "self_service":
        locations = locations.filter(
            Q(location_type=Location.LocationType.SELF_SERVICE)
            | Q(location_type=Location.LocationType.BOTH)
        )
    elif location_type == "staff_service":
        locations = locations.filter(
            Q(location_type=Location.LocationType.STAFF_SERVICE)
            | Q(location_type=Location.LocationType.BOTH)
        )

    return locations.order_by("address")


def get_active_location_by_slug(slug):
    """Найти активную точку по slug или вернуть None."""
    return list_active_locations().filter(slug=slug).first()