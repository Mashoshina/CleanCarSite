from django.core.validators import RegexValidator
from django.db import models

from apps.locations.models import Location


class Booking(models.Model):
    """Бронь на посещение точки автомойки."""

    class BookingType(models.IntegerChoices):
        SELF_SERVICE = 0, "Самообслуживание"
        STAFF_SERVICE = 1, "Обслуживание персоналом"

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
                regex=r"^\+?[0-9\s\-\(\)]+$",
                message="Телефон должен содержать только цифры, пробелы, +, -, ()",
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
    booking_type = models.PositiveSmallIntegerField(
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