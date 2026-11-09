from django.core.validators import RegexValidator
from django.db import models

from apps.locations.models import Location


class Booking(models.Model):
    """Бронь на посещение точки автомойки."""

    class BookingType(models.TextChoices):
        SELF_SERVICE = "self_service", "Самообслуживание"
        STAFF_SERVICE = "staff_service", "Обслуживание персоналом"

    class ConfirmationStatus(models.TextChoices):
        CONFIRMED = "Y", "Подтверждено"
        NOT_CONFIRMED = "N", "Не подтверждено"

    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="Точка",
    )
    client_name = models.CharField(
        max_length=150,
        verbose_name="Имя клиента",
    )
    client_phone = models.CharField(
        max_length=20,
        validators=[
           RegexValidator(
                regex=r"^\+7\d{10}$",
                message="Укажите номер в формате +7XXXXXXXXXX.",
            )
        ],
        verbose_name="Телефон клиента",
    )
    booking_date = models.DateField(
        verbose_name="Дата",
    )
    booking_time = models.TimeField(
        verbose_name="Время",
    )
    booking_type = models.CharField(
        max_length=20,
        choices=BookingType.choices,
        verbose_name="Тип",
    )
    confirmation_status = models.CharField(
        max_length=1,
        choices=ConfirmationStatus.choices,
        default=ConfirmationStatus.NOT_CONFIRMED,
        verbose_name="Статус подтверждения",
    )

    def __str__(self):
        return f"{self.client_name} — {self.location}"

    class Meta:
        verbose_name = "Бронь"
        verbose_name_plural = "Брони"
        ordering = ["booking_date", "booking_time"]