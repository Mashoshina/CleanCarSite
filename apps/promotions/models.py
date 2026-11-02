from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Promotion(models.Model):
    """Акция/скидка."""

    title = models.CharField(
        max_length=200,
        verbose_name="Название акции",
    )
    conditions = models.TextField(
        verbose_name="Условия акции",
    )
    discount_percent = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(5), MaxValueValidator(100)],
        verbose_name="Процент скидки",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"
        ordering = ["title"]