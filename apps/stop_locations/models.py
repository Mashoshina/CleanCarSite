from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q

from apps.locations.models import Location


class StopLocation(models.Model):
    """Период отключения точки автомойки по датам."""

    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="stop_periods",
        verbose_name="Точка",
    )
    start_date = models.DateField(
        verbose_name="Дата начала отключения",
    )
    end_date = models.DateField(
        verbose_name="Дата окончания отключения",
    )

    def clean(self):
        super().clean()

        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError(
                    {
                        "end_date": (
                            "Дата окончания не может быть раньше даты начала."
                        ),
                    }
                )

            if self.location_id:
                overlapping_periods = StopLocation.objects.filter(
                    location_id=self.location_id,
                    start_date__lte=self.end_date,
                    end_date__gte=self.start_date,
                )

                if self.pk:
                    overlapping_periods = overlapping_periods.exclude(
                        pk=self.pk
                    )

                if overlapping_periods.exists():
                    raise ValidationError(
                        "Периоды отключения одной точки не должны пересекаться."
                    )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.location} ({self.start_date} — {self.end_date})"

    class Meta:
        verbose_name = "Отключение точки"
        verbose_name_plural = "Отключения точек"
        ordering = ["start_date"]
        constraints = [
            models.CheckConstraint(
                condition=Q(end_date__gte=F("start_date")),
                name="stop_location_end_date_gte_start_date",
            ),
        ]