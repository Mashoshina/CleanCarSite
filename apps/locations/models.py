
from django.db import models
from django.utils.text import slugify


class Location(models.Model):
    """Точка сети автомоек CleanCar."""

    class LocationType(models.IntegerChoices):
        SELF_SERVICE = 0, "Самообслуживание"
        STAFF_SERVICE = 1, "Обслуживание персоналом"
        BOTH = 2, "Самообслуживание и обслуживание персоналом"

    location_type = models.PositiveSmallIntegerField(
        choices=LocationType.choices,
        verbose_name="Тип точки",
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Номер телефона",
    )
    address = models.CharField(
        max_length=255,
        verbose_name="Адрес",
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        verbose_name="Slug",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.address, allow_unicode=True)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = "Точка автомойки"
        verbose_name_plural = "Точки автомоек"
