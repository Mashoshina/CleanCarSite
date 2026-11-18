from rest_framework import serializers

from .models import Location


class LocationSerializer(serializers.ModelSerializer):
    available_booking_types = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = (
            "id",
            "slug",
            "address",
            "phone",
            "latitude",
            "longitude",
            "location_type",
            "available_booking_types",
        )

    def get_available_booking_types(self, location):
        if location.location_type == Location.LocationType.BOTH:
            return [
                Location.LocationType.SELF_SERVICE,
                Location.LocationType.STAFF_SERVICE,
            ]

        return [location.location_type]