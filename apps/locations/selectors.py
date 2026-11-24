from datetime import date, time

from django.db.models import Q
from django.utils import timezone
from apps.bookings.selectors import get_bookings_for_location_date

from datetime import date, time
from django.utils import timezone
from apps.bookings.selectors import get_bookings_for_location_date

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

    if len(query) < 2:
        return Location.objects.none()

    return Location.objects.filter(
        is_active=True,
        address__icontains=query,
    ).order_by("address")[:limit]


def list_active_locations(location_type=None, query=None):
    """Вернуть активные точки с необязательной фильтрацией по формату и адресу."""
    locations = Location.objects.filter(is_active=True)

    if location_type == Location.LocationType.SELF_SERVICE:
        locations = locations.filter(
            Q(location_type=Location.LocationType.SELF_SERVICE)
            | Q(location_type=Location.LocationType.BOTH)
        )
    elif location_type == Location.LocationType.STAFF_SERVICE:
        locations = locations.filter(
            Q(location_type=Location.LocationType.STAFF_SERVICE)
            | Q(location_type=Location.LocationType.BOTH)
        )
    # both и отсутствие типа означают: показать точки всех форматов.

    query = (query or "").strip()
    if query:
        locations = locations.filter(address__icontains=query)

    return locations.order_by("address")


def get_available_times_by_location(locations, selected_date: date):
    """Рассчитать свободные часовые слоты для точек на выбранную дату."""
    locations = list(locations)
    today = timezone.localdate()

    if selected_date < today:
        return {location.pk: [] for location in locations}

    first_hour = 0

    if selected_date == today:
        now = timezone.localtime()
        first_hour = now.hour

        # Если текущий час уже начался, запись возможна со следующего часа.
        if now.minute or now.second or now.microsecond:
            first_hour += 1

    available_times = {}

    for location in locations:
        bookings = get_bookings_for_location_date(
            location_id=location.pk,
            booking_date=selected_date,
        )

        booked_minutes = [
            booking.booking_time.hour * 60 + booking.booking_time.minute
            for booking in bookings
        ]

        free_slots = []

        for hour in range(first_hour, 24):
            slot_start = hour * 60
            slot_end = slot_start + 60

            overlaps_booking = any(
                booking_start < slot_end
                and booking_start + 60 > slot_start
                for booking_start in booked_minutes
            )

            if not overlaps_booking:
                free_slots.append(time(hour=hour).strftime("%H:%M"))

        available_times[location.pk] = free_slots

    return available_times


def get_active_location_by_slug(slug):
    """Найти активную точку по slug или вернуть None."""
    return list_active_locations().filter(slug=slug).first()