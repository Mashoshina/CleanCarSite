from datetime import date, time

from .models import Booking


BOOKING_DURATION_MINUTES = 60


def get_bookings_for_location_date(
    location_id: int,
    booking_date: date,
):
    """Вернуть брони точки за указанную дату."""
    return (
        Booking.objects.filter(
            location_id=location_id,
            booking_date=booking_date,
        )
        .select_related("location")
        .order_by("booking_time")
    )


def get_bookings_overlapping_slot(
    location_id: int,
    booking_date: date,
    booking_time: time,
):
    """Вернуть брони, пересекающиеся с часовым слотом."""
    slot_start = booking_time.hour * 60 + booking_time.minute
    slot_end = slot_start + BOOKING_DURATION_MINUTES

    bookings = get_bookings_for_location_date(location_id, booking_date)

    return [
        booking
        for booking in bookings
        if (
            booking.booking_time.hour * 60 + booking.booking_time.minute
            < slot_end
            and booking.booking_time.hour * 60 + booking.booking_time.minute
            + BOOKING_DURATION_MINUTES
            > slot_start
        )
    ]


def is_booking_slot_available(
    location_id: int,
    booking_date: date,
    booking_time: time,
) -> bool:
    """Проверить, свободен ли часовой слот точки."""
    return not get_bookings_overlapping_slot(
        location_id=location_id,
        booking_date=booking_date,
        booking_time=booking_time,
    )