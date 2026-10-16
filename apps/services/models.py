
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify


class Service(models.Model):
    """Услуга сети автомоек CleanCar."""

    name = models.CharField(
        max_length=150,
        verbose_name="Название услуги",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Цена",
    )
    service_type = models.CharField(
        max_length=100,
        verbose_name="Тип услуги",
    )
    vehicle_type = models.CharField(
        max_length=100,
        verbose_name="Тип транспортного средства",
    )
    slug = models.SlugField(
        max_length=180,
        unique=True,
        blank=True,
        verbose_name="Slug",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name, allow_unicode=True)
            slug = base_slug
            suffix = 2

            while (
                Service.objects.filter(slug=slug)
                .exclude(pk=self.pk)
                .exists()
            ):
                slug = f"{base_slug}-{suffix}"
                suffix += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ["name"]
