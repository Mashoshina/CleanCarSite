from datetime import date, time
from time import strptime

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.locations.models import Location
from apps.locations.selectors import location_supports_booking_type

from .models import Booking
from .selectors import (
    get_bookings_for_location_date,
    is_booking_slot_available,
)
from .serializers import BookingCreateSerializer, BookingReadSerializer


class BookingListCreateView(APIView):
    """
    GET: получить брони выбранной точки на дату.
    POST: создать бронь.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        location_id = request.query_params.get("location")
        booking_date_value = request.query_params.get("date")
        booking_time_value = request.query_params.get("time")

        if not location_id or not booking_date_value:
            return Response(
                {"detail": "Укажите параметры location и date."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            location_id = int(location_id)
            booking_date = date.fromisoformat(booking_date_value)
        except (TypeError, ValueError):
            return Response(
                {"detail": "Некорректный location или date. Используйте date=YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if booking_time_value:
            try:
                requested_time = time.fromisoformat(booking_time_value)
            except ValueError:
                return Response(
                    {"detail": "Некорректное время. Используйте формат HH:MM."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            bookings = get_bookings_for_location_date(
                location_id,
                booking_date,
            )
            slot_start = requested_time.hour * 60 + requested_time.minute
            slot_end = slot_start + 60

            bookings = [
                booking
                for booking in bookings
                if (
                    booking.booking_time.hour * 60 + booking.booking_time.minute
                    < slot_end
                    and booking.booking_time.hour * 60
                    + booking.booking_time.minute
                    + 60
                    > slot_start
                )
            ]
        else:
            bookings = get_bookings_for_location_date(
                location_id,
                booking_date,
            )

        return Response(BookingReadSerializer(bookings, many=True).data)

    def post(self, request):
        serializer = BookingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated = serializer.validated_data
        location = validated["location"]
        booking_date = validated["booking_date"]
        booking_time = validated["booking_time"]
        booking_type = validated["booking_type"]

        # Блокируем запись точки на время проверки и создания,
        # чтобы параллельные запросы не заняли один и тот же слот.
        with transaction.atomic():
            locked_location = get_object_or_404(
                Location.objects.select_for_update(),
                pk=location.pk,
                is_active=True,
            )

            if not location_supports_booking_type(
                locked_location,
                booking_type,
            ):
                return Response(
                    {"booking_type": "Этот формат недоступен в выбранной точке."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not is_booking_slot_available(
                location_id=locked_location.pk,
                booking_date=booking_date,
                booking_time=booking_time,
            ):
                return Response(
                    {"booking_time": "Это время уже занято. Выберите другой час."},
                    status=status.HTTP_409_CONFLICT,
                )

            booking = serializer.save(location=locked_location)

        return Response(
            BookingReadSerializer(booking).data,
            status=status.HTTP_201_CREATED,
        )


class BookingDeleteView(APIView):
    """Удалить бронь. Доступно только администратору."""

    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)