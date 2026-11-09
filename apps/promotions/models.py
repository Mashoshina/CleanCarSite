from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify

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
                Promotion.objects.filter(slug=slug)
                .exclude(pk=self.pk)
                .exists()
            ):
                slug = f"{base_slug}-{suffix}"
                suffix += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"
        ordering = ["title"]