
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models
from django.utils.text import slugify


class Location(models.Model):
    """Точка сети автомоек CleanCar."""

    class LocationType(models.TextChoices):
        SELF_SERVICE = "self_service", "Самообслуживание"
        STAFF_SERVICE = "staff_service", "Обслуживание персоналом"
        BOTH = "both", "Самообслуживание и обслуживание персоналом"

    location_type = models.CharField(
        max_length=20,
        choices=LocationType.choices,
        verbose_name="Тип точки",
    )
    phone = models.CharField(
        max_length=12,
        validators=[
            RegexValidator(
                regex=r"^\+7\d{10}$",
                message="Укажите номер в формате +7XXXXXXXXXX.",
            ),
        ],
        verbose_name="Номер телефона",
        help_text="Формат: +7 и ещё 10 цифр.",
    )
    address = models.CharField(
        max_length=255,
        verbose_name="Адрес",
        help_text="Например: Челябинск, Ленина, 15.",
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[
            MinValueValidator(-90),
            MaxValueValidator(90),
        ],
        verbose_name="Широта",
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[
            MinValueValidator(-180),
            MaxValueValidator(180),
        ],
        verbose_name="Долгота",
    )
    is_active = models.BooleanField(
        default=True,
        choices=[
            (True, "Активна"),
            (False, "Не активна"),
        ],
        verbose_name="Статус",
    )
    slug = models.SlugField(
        max_length=300,
        unique=True,
        blank=True,
        verbose_name="Slug",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.address, allow_unicode=True) or "location"
            slug = base_slug
            suffix = 2

            while (
                Location.objects.filter(slug=slug)
                .exclude(pk=self.pk)
                .exists()
            ):
                slug = f"{base_slug}-{suffix}"
                suffix += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = "Точка автомойки"
        verbose_name_plural = "Точки автомоек"
        ordering = ["address"]
