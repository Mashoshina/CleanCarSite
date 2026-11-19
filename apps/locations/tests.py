from django.test import SimpleTestCase

from .models import Location
from .selectors import location_supports_booking_type


class LocationSupportsBookingTypeTests(SimpleTestCase):
    def make_location(self, location_type):
        return Location(location_type=location_type)

    def test_self_service_location_accepts_self_service_booking(self):
        location = self.make_location(Location.LocationType.SELF_SERVICE)

        self.assertTrue(
            location_supports_booking_type(
                location,
                Location.LocationType.SELF_SERVICE,
            )
        )

    def test_self_service_location_rejects_staff_service_booking(self):
        location = self.make_location(Location.LocationType.SELF_SERVICE)

        self.assertFalse(
            location_supports_booking_type(
                location,
                Location.LocationType.STAFF_SERVICE,
            )
        )

    def test_staff_service_location_accepts_staff_service_booking(self):
        location = self.make_location(Location.LocationType.STAFF_SERVICE)

        self.assertTrue(
            location_supports_booking_type(
                location,
                Location.LocationType.STAFF_SERVICE,
            )
        )

    def test_staff_service_location_rejects_self_service_booking(self):
        location = self.make_location(Location.LocationType.STAFF_SERVICE)

        self.assertFalse(
            location_supports_booking_type(
                location,
                Location.LocationType.SELF_SERVICE,
            )
        )

    def test_both_location_accepts_both_booking_types(self):
        location = self.make_location(Location.LocationType.BOTH)

        for booking_type in (
            Location.LocationType.SELF_SERVICE,
            Location.LocationType.STAFF_SERVICE,
        ):
            with self.subTest(booking_type=booking_type):
                self.assertTrue(
                    location_supports_booking_type(location, booking_type)
                )

    def test_both_is_not_a_valid_booking_type(self):
        location = self.make_location(Location.LocationType.BOTH)

        self.assertFalse(
            location_supports_booking_type(
                location,
                Location.LocationType.BOTH,
            )
        )

    def test_unknown_booking_type_is_rejected(self):
        location = self.make_location(Location.LocationType.BOTH)

        self.assertFalse(
            location_supports_booking_type(location, "unknown")
        )