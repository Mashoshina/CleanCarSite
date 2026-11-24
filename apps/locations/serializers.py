from rest_framework import serializers

from .models import Location


class LocationSerializer(serializers.ModelSerializer):
    available_booking_types = serializers.SerializerMethodField()
    available_times = serializers.SerializerMethodField()

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
            "available_times",
        )

    def get_available_booking_types(self, location):
        if location.location_type == Location.LocationType.BOTH:
            return [
                Location.LocationType.SELF_SERVICE,
                Location.LocationType.STAFF_SERVICE,
            ]

        return [location.location_type]
    
    def get_available_times(self, location):
        return self.context.get("available_times", {}).get(location.pk, [])
    
class LocationSuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("id", "slug", "address")