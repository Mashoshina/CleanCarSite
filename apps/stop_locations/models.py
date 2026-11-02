from django.core.exceptions import ValidationError
from django.db import models

# Импортируем модель Location из приложения locations
from apps.locations.models import Location


class StopLocation(models.Model):
    """Период остановки работы точки автомойки."""

    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="stop_periods",
        verbose_name="Точка",
    )
    start_date = models.DateField(
        verbose_name="Дата начала остановки работы точки",
    )
    end_date = models.DateField(
        verbose_name="Дата конца остановки работы точки",
    )

    def clean(self):
        super().clean()
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError(
                {
                    "end_date": "Дата окончания не может быть раньше даты начала.",
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.location} ({self.start_date} — {self.end_date})"

    class Meta:
        verbose_name = "Остановка точки"
        verbose_name_plural = "Остановки точек"
        ordering = ["start_date"]