from django.utils import timezone
from rest_framework import serializers

from apps.locations.models import Location
from apps.locations.selectors import location_supports_booking_type

from .models import Booking
from .selectors import is_booking_slot_available


class BookingReadSerializer(serializers.ModelSerializer):
    """Публичный ответ API без персональных данных клиента."""

    location_address = serializers.CharField(
        source="location.address",
        read_only=True,
    )

    class Meta:
        model = Booking
        fields = (
            "id",
            "location",
            "location_address",
            "booking_date",
            "booking_time",
            "booking_type",
            "confirmation_status",
        )


class BookingCreateSerializer(serializers.ModelSerializer):
    """Проверка данных и создание брони."""

    location = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.filter(is_active=True),
    )

    class Meta:
        model = Booking
        fields = (
            "location",
            "client_name",
            "client_phone",
            "booking_date",
            "booking_time",
            "booking_type",
        )

    def validate(self, attrs):
        location = attrs["location"]
        booking_date = attrs["booking_date"]
        booking_time = attrs["booking_time"]
        booking_type = attrs["booking_type"]

        if not location.is_active:
            raise serializers.ValidationError({
                "location": "Эта точка сейчас не принимает записи.",
            })

        if not location_supports_booking_type(location, booking_type):
            raise serializers.ValidationError({
                "booking_type": "Этот формат недоступен в выбранной точке.",
            })

        if (
            booking_time.minute != 0
            or booking_time.second != 0
            or booking_time.microsecond != 0
        ):
            raise serializers.ValidationError({
                "booking_time": "Запись доступна только на начало часа.",
            })

        local_now = timezone.localtime()
        today = local_now.date()

        if booking_date < today:
            raise serializers.ValidationError({
                "booking_date": "Нельзя записаться на прошедшую дату.",
            })

        if booking_date == today and booking_time < local_now.time().replace(
            minute=0,
            second=0,
            microsecond=0,
        ):
            raise serializers.ValidationError({
                "booking_time": "Нельзя записаться на прошедшее время.",
            })

        if not is_booking_slot_available(
            location_id=location.pk,
            booking_date=booking_date,
            booking_time=booking_time,
        ):
            raise serializers.ValidationError({
                "booking_time": "Это время уже занято. Выберите другой час.",
            })

        return attrs