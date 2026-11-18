from django.db.models import Q

from .models import Location


def list_active_locations(location_type=None, query=None):
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

    if query:
        locations = locations.filter(address__icontains=query.strip())

    return locations.order_by("address")


def get_active_location_by_slug(slug):
    """Найти активную точку по slug или вернуть None."""
    return list_active_locations().filter(slug=slug).first()